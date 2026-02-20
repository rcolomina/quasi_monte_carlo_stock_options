"""
Off-chain pricing oracle for Solana DeFi options protocol.

Computes option prices using QMC methods and submits to on-chain program.
Runs as a crank (Clockwork automation) or standalone service.
"""

import asyncio
import time
from typing import Dict, List
import numpy as np
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from anchorpy import Provider, Wallet

# Your pricing models
from qmc_options import (
    generators, analytical, jump_diffusion, stochastic_volatility
)


class SolanaPricingOracle:
    """
    Pricing oracle that computes option prices off-chain and submits to Solana.
    """

    def __init__(self, rpc_url: str, keypair: Keypair, program_id: Pubkey):
        """
        Parameters
        ----------
        rpc_url : str
            Solana RPC endpoint (mainnet-beta, devnet, etc.)
        keypair : Keypair
            Authority keypair for signing price updates
        program_id : Pubkey
            Your options program address
        """
        self.client = AsyncClient(rpc_url)
        self.keypair = keypair
        self.program_id = program_id

        # Calibrated models (updated periodically)
        self.models = {}

        # QMC points (pre-generated for speed)
        self.qmc_points_1d = generators.halton([2], 10000)[:, 0]
        self.qmc_points_2d = generators.good_lattice_points(12)

    async def fetch_pyth_price(self, pyth_account: Pubkey) -> Dict:
        """
        Fetch current price from Pyth oracle.

        Pyth accounts:
        - SOL/USD: H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG
        - BTC/USD: GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU
        - ETH/USD: JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB

        Returns
        -------
        dict
            {'price': float, 'conf': float, 'expo': int, 'publish_time': int}
        """
        from pythclient.pythaccounts import PythPriceAccount

        # Fetch account data
        account_info = await self.client.get_account_info(pyth_account)
        price_account = PythPriceAccount(pyth_account, account_info.value.data)

        # Extract price
        price_data = price_account.aggregate_price_info

        return {
            'price': price_data.price * (10 ** price_data.exponent),
            'confidence': price_data.confidence * (10 ** price_data.exponent),
            'expo': price_data.exponent,
            'publish_time': price_account.timestamp,
            'status': price_data.status
        }

    def calibrate_models(self, asset: str, historical_prices: np.ndarray):
        """
        Calibrate Heston and Merton models from historical data.

        In production, this runs daily or when volatility regime changes.
        """
        from qmc_options.market_data import (
            calculate_historical_volatility,
            estimate_jump_parameters_from_history
        )

        # Historical volatility
        hist_vol = calculate_historical_volatility(historical_prices)

        # Jump parameters
        jump_params = estimate_jump_parameters_from_history(historical_prices)

        # Heston parameters (simplified calibration)
        # In production, calibrate to options market if available
        heston_params = {
            'V0': hist_vol ** 2,
            'kappa': 2.0,
            'theta': hist_vol ** 2,
            'sigma_v': 0.3,
            'rho': -0.7  # Leverage effect
        }

        self.models[asset] = {
            'heston': heston_params,
            'merton': jump_params,
            'hist_vol': hist_vol
        }

        print(f"Calibrated {asset}:")
        print(f"  Heston V0: {heston_params['V0']:.4f}")
        print(f"  Jump λ: {jump_params['lambda_jump']:.2f}/year")

    def price_option_heston(self, S0: float, K: float, r: float, T: float,
                           asset: str, option_type: str = 'call') -> Dict:
        """
        Price option using calibrated Heston model.

        Returns
        -------
        dict
            {'price': float, 'delta': float, 'gamma': float, 'vega': float}
        """
        if asset not in self.models:
            raise ValueError(f"No calibrated model for {asset}")

        params = self.models[asset]['heston']

        # Price with Heston
        price, std_err = stochastic_volatility.european_call_heston_mc(
            S0=S0,
            V0=params['V0'],
            K=K,
            r=r,
            delta=0.0,  # Crypto has no dividends
            T=T,
            kappa=params['kappa'],
            theta=params['theta'],
            sigma_v=params['sigma_v'],
            rho=params['rho'],
            N=5000,
            use_qe=True
        )

        # Approximate Greeks (numerical differentiation)
        dS = S0 * 0.01
        price_up, _ = stochastic_volatility.european_call_heston_mc(
            S0=S0 + dS, V0=params['V0'], K=K, r=r, delta=0.0, T=T,
            kappa=params['kappa'], theta=params['theta'],
            sigma_v=params['sigma_v'], rho=params['rho'],
            N=1000, use_qe=True
        )

        delta = (price_up - price) / dS

        return {
            'price': price,
            'std_error': std_err,
            'delta': delta,
            'gamma': 0.0,  # Would need more samples
            'vega': 0.0,
            'model': 'heston'
        }

    def price_option_merton(self, S0: float, K: float, r: float, T: float,
                           asset: str) -> Dict:
        """Price option using calibrated Merton jump-diffusion."""
        if asset not in self.models:
            raise ValueError(f"No calibrated model for {asset}")

        params = self.models[asset]['merton']

        price, std_err = jump_diffusion.european_call_merton_mc(
            S0=S0,
            K=K,
            r=r,
            delta=0.0,
            sigma=params['continuous_vol'],
            T=T,
            lambda_jump=params['lambda_jump'],
            mu_jump=params['mu_jump'],
            sigma_jump=params['sigma_jump'],
            points=self.qmc_points_1d
        )

        return {
            'price': price,
            'std_error': std_err,
            'model': 'merton'
        }

    async def update_prices_on_chain(self, prices: Dict[str, Dict]):
        """
        Submit computed prices to Solana program.

        Parameters
        ----------
        prices : dict
            {
                'SOL-100-CALL-30D': {'price': 5.23, 'delta': 0.65, ...},
                'BTC-50000-PUT-7D': {'price': 1234.56, 'delta': -0.45, ...}
            }
        """
        # This would use Anchor to call your Solana program
        # Pseudo-code:

        for option_id, price_data in prices.items():
            # Prepare instruction data
            instruction_data = {
                'option_id': option_id,
                'price': int(price_data['price'] * 1e6),  # 6 decimals
                'delta': int(price_data['delta'] * 1e6),
                'timestamp': int(time.time()),
                'model_type': price_data['model']
            }

            # Sign and send transaction
            # tx = await program.rpc.update_oracle_price(
            #     instruction_data,
            #     ctx=Context(
            #         accounts={
            #             'oracle': oracle_pda,
            #             'authority': self.keypair.pubkey(),
            #         },
            #         signers=[self.keypair]
            #     )
            # )

            print(f"Updated {option_id}: ${price_data['price']:.2f}")

    async def run_crank(self, interval_seconds: int = 300):
        """
        Main crank loop - compute and update prices every N seconds.

        Parameters
        ----------
        interval_seconds : int
            Update frequency (default 5 minutes)
        """
        print(f"Starting pricing oracle crank (interval: {interval_seconds}s)")

        iteration = 0
        while True:
            iteration += 1
            print(f"\n=== Crank Iteration {iteration} ===")

            try:
                # 1. Fetch current Pyth prices
                sol_pyth = Pubkey.from_string("H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG")
                btc_pyth = Pubkey.from_string("GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU")

                sol_price_data = await self.fetch_pyth_price(sol_pyth)
                btc_price_data = await self.fetch_pyth_price(btc_pyth)

                print(f"SOL/USD: ${sol_price_data['price']:.2f}")
                print(f"BTC/USD: ${btc_price_data['price']:.2f}")

                # 2. Compute option prices
                prices_to_update = {}

                # Example: SOL 7-day ATM call
                r = 0.05  # Risk-free rate (approximate from USDC staking)
                T = 7 / 365.0

                sol_call_price = self.price_option_heston(
                    S0=sol_price_data['price'],
                    K=sol_price_data['price'],  # ATM
                    r=r,
                    T=T,
                    asset='SOL',
                    option_type='call'
                )

                prices_to_update['SOL-ATM-CALL-7D'] = sol_call_price

                # 3. Submit to Solana
                await self.update_prices_on_chain(prices_to_update)

                # 4. Sleep until next iteration
                await asyncio.sleep(interval_seconds)

            except Exception as e:
                print(f"Error in crank iteration: {e}")
                await asyncio.sleep(60)  # Wait 1 min before retry


async def main():
    """Example usage."""
    # Load keypair (in production, use secure key management)
    # keypair = Keypair.from_base58_string("YOUR_PRIVATE_KEY")
    keypair = Keypair()  # Placeholder

    # Initialize oracle
    oracle = SolanaPricingOracle(
        rpc_url="https://api.devnet.solana.com",
        keypair=keypair,
        program_id=Pubkey.from_string("11111111111111111111111111111111")  # Your program
    )

    # Calibrate models (using dummy data for demo)
    historical_sol = np.random.lognormal(0, 0.02, 365)  # Simulated daily returns
    oracle.calibrate_models('SOL', historical_sol)

    # Run crank
    await oracle.run_crank(interval_seconds=300)


if __name__ == "__main__":
    # Install: pip install solana solders anchorpy pythclient
    asyncio.run(main())
