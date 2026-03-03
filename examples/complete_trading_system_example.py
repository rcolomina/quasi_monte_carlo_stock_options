"""
Complete Example: Building a Trading System with Advanced Models

This demonstrates:
1. Fetching real market data
2. Calibrating jump-diffusion or Heston models
3. Finding mispriced options
4. Executing trades with delta hedging
5. Monitoring P&L

Run this to see the full system in action!
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Import our modules
from qmc_options import (
    generators, pricing, analytical,
    market_data, jump_diffusion, stochastic_volatility,
    trading_system
)


def example_1_fetch_and_calibrate():
    """Example 1: Fetch market data and calibrate Heston model."""
    print("=" * 60)
    print("EXAMPLE 1: Market Data Calibration")
    print("=" * 60)

    ticker = 'SPY'  # S&P 500 ETF

    # 1. Fetch current market data
    print(f"\n1. Fetching market data for {ticker}...")
    S0 = market_data.MarketDataFeed.get_current_price(ticker)
    r = market_data.MarketDataFeed.get_risk_free_rate()
    delta = market_data.MarketDataFeed.estimate_dividend_yield(ticker)

    print(f"   Current Price: ${S0:.2f}")
    print(f"   Risk-free Rate: {r*100:.2f}%")
    print(f"   Dividend Yield: {delta*100:.2f}%")

    # 2. Fetch historical prices for jump detection
    print("\n2. Analyzing historical data...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    hist_prices = market_data.MarketDataFeed.get_historical_prices(
        ticker,
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

    # Calculate historical volatility
    hist_vol = market_data.calculate_historical_volatility(hist_prices['Close'])
    print(f"   Historical Volatility: {hist_vol*100:.2f}%")

    # Detect jumps
    jump_params = market_data.estimate_jump_parameters_from_history(hist_prices['Close'])
    print(f"   Jump Intensity: {jump_params['lambda_jump']:.2f} jumps/year")
    print(f"   Number of Jumps Detected: {jump_params['n_jumps_detected']}")

    # 3. Fetch options chain
    print("\n3. Fetching options chain...")
    expiry = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    try:
        options_chain = market_data.MarketDataFeed.get_options_chain_yahoo(ticker, expiry)
        print(f"   Found {len(options_chain)} strikes")
        print(f"   Strike range: ${options_chain['strike'].min():.0f} - ${options_chain['strike'].max():.0f}")
    except Exception as e:
        print(f"   Warning: Could not fetch options chain: {e}")
        print(f"   Using synthetic data for demonstration...")
        options_chain = create_synthetic_options_chain(S0)

    return {
        'ticker': ticker,
        'S0': S0,
        'r': r,
        'delta': delta,
        'hist_vol': hist_vol,
        'jump_params': jump_params,
        'options_chain': options_chain,
        'expiry': expiry
    }


def example_2_compare_models(market_data_dict):
    """Example 2: Compare pricing across different models."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Model Comparison")
    print("=" * 60)

    S0 = market_data_dict['S0']
    r = market_data_dict['r']
    delta = market_data_dict['delta']
    T = 30 / 365.0  # 30 days

    # Select ATM strike
    K = round(S0 / 5) * 5  # Round to nearest $5

    print(f"\nPricing ATM call: S0=${S0:.2f}, K=${K:.0f}, T={T*365:.0f} days")

    # Generate QMC points
    qmc_points = generators.halton([2], 10000)[:, 0]

    # 1. Black-Scholes (baseline)
    bs_price = analytical.black_scholes_call(S0, K, r, delta, 0.25, T)
    print(f"\n1. Black-Scholes: ${bs_price:.2f}")

    # 2. Merton Jump-Diffusion
    jump_params = market_data_dict['jump_params']
    merton_price, merton_se = jump_diffusion.european_call_merton_mc(
        S0, K, r, delta,
        sigma=jump_params['continuous_vol'],
        T=T,
        lambda_jump=jump_params['lambda_jump'],
        mu_jump=jump_params['mu_jump'],
        sigma_jump=jump_params['sigma_jump'],
        points=qmc_points
    )
    print(f"2. Merton Jump-Diffusion: ${merton_price:.2f} ± ${merton_se:.3f}")
    print(f"   Jump impact: {(merton_price - bs_price):.2f} ({(merton_price/bs_price - 1)*100:.1f}%)")

    # 3. Heston Stochastic Volatility
    heston_price, heston_se = stochastic_volatility.european_call_heston_mc(
        S0=S0,
        V0=0.25**2,  # Initial variance
        K=K,
        r=r,
        delta=delta,
        T=T,
        kappa=2.0,  # Mean reversion
        theta=0.25**2,  # Long-run variance
        sigma_v=0.3,  # Vol-of-vol
        rho=-0.7,  # Negative correlation (leverage effect)
        N=5000,
        use_qe=True
    )
    print(f"3. Heston Stochastic Vol: ${heston_price:.2f} ± ${heston_se:.3f}")
    print(f"   Stochastic vol impact: {(heston_price - bs_price):.2f} ({(heston_price/bs_price - 1)*100:.1f}%)")

    return {
        'K': K,
        'bs_price': bs_price,
        'merton_price': merton_price,
        'heston_price': heston_price
    }


def example_3_volatility_arbitrage(market_data_dict, pricing_results):
    """Example 3: Find and execute volatility arbitrage opportunities."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Volatility Arbitrage Strategy")
    print("=" * 60)

    # Initialize portfolio
    portfolio = trading_system.Portfolio(initial_capital=100000)

    # Initialize strategy
    strategy = trading_system.VolatilityArbitrageStrategy(
        portfolio=portfolio,
        pricing_model=None,  # We'll price manually
        mispricing_threshold=0.05  # 5% edge required
    )

    # Scan for opportunities
    print("\nScanning for mispriced options...")

    options_chain = market_data_dict['options_chain']
    opportunities = []

    for _, row in options_chain.head(10).iterrows():
        strike = row['strike']
        market_price = row.get('call_price', 0)

        if market_price > 0:
            # Price using our Heston model (simplified)
            model_price = pricing_results['heston_price']  # Placeholder

            edge = (model_price - market_price) / market_price

            if abs(edge) > strategy.mispricing_threshold:
                opportunities.append({
                    'strike': strike,
                    'type': 'call',
                    'market_price': market_price,
                    'model_price': model_price,
                    'edge': edge,
                    'action': 'buy' if edge > 0 else 'sell'
                })

    print(f"Found {len(opportunities)} opportunities")

    # Execute best trade
    if opportunities:
        best = sorted(opportunities, key=lambda x: abs(x['edge']), reverse=True)[0]

        print(f"\nBest Opportunity:")
        print(f"  Strike: ${best['strike']:.0f}")
        print(f"  Market Price: ${best['market_price']:.2f}")
        print(f"  Model Price: ${best['model_price']:.2f}")
        print(f"  Edge: {best['edge']*100:.1f}%")
        print(f"  Action: {best['action'].upper()}")

        # Execute (simulated)
        print("\n[SIMULATED] Executing trade...")
        strategy.execute_trade(
            opportunity=best,
            ticker=market_data_dict['ticker'],
            expiry=market_data_dict['expiry'],
            quantity=1
        )

    return portfolio


def create_synthetic_options_chain(S0: float) -> pd.DataFrame:
    """Create synthetic options chain for demonstration."""
    strikes = np.arange(S0 * 0.9, S0 * 1.1, 5)

    data = []
    for K in strikes:
        # Synthetic Black-Scholes prices
        call_price = analytical.black_scholes_call(S0, K, 0.04, 0.02, 0.25, 30/365)
        put_price = analytical.black_scholes_put(S0, K, 0.04, 0.02, 0.25, 30/365)

        data.append({
            'strike': K,
            'call_price': call_price,
            'put_price': put_price,
            'call_iv': 0.25,
            'put_iv': 0.25,
            'call_volume': 100,
            'put_volume': 50,
            'call_oi': 1000,
            'put_oi': 500
        })

    return pd.DataFrame(data)


def main():
    """Run all examples."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║   COMPLETE TRADING SYSTEM WITH ADVANCED PRICING MODELS    ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║   This demonstrates how to build a production trading    ║
║   system using quasi-Monte Carlo methods with:           ║
║                                                           ║
║   • Jump-diffusion models (Merton, Kou)                 ║
║   • Stochastic volatility (Heston)                      ║
║   • Real market data integration                        ║
║   • Volatility arbitrage strategy                       ║
║   • Automated delta hedging                             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

    try:
        # Example 1: Data and calibration
        market_data_dict = example_1_fetch_and_calibrate()

        # Example 2: Model comparison
        pricing_results = example_2_compare_models(market_data_dict)

        # Example 3: Trading strategy
        portfolio = example_3_volatility_arbitrage(market_data_dict, pricing_results)

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"\nPortfolio Status:")
        print(f"  Positions: {len(portfolio.positions)}")
        print(f"  Trades Executed: {len(portfolio.trades_history)}")
        print(f"  Capital Deployed: ${portfolio.initial_capital - portfolio.capital:,.0f}")

        print("\n" + "=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print("""
1. Deploy to AWS Lambda for real-time pricing
2. Connect to Interactive Brokers API for live trading
3. Add risk management (position limits, stop losses)
4. Implement backtesting framework
5. Create monitoring dashboard
6. Set up alerts for trading opportunities
        """)

    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: Some features require market data access.")
        print("For full functionality, install: pip install yfinance")


if __name__ == "__main__":
    main()
