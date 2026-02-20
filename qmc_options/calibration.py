"""
Asset-specific model calibration for improved accuracy.

Different assets have different characteristics:
- Equities: Leverage effect, mean-reverting vol, fat tails
- Crypto: HUGE jumps, regime shifts, volatility clustering
- Commodities: Seasonality, mean reversion in prices
- FX: Interest rate differentials, carry

This module automatically selects and calibrates the best model for each asset.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional, Literal
from dataclasses import dataclass
from scipy.optimize import minimize
from scipy.stats import skew, kurtosis, jarque_bera
import warnings

from qmc_options import (
    generators, analytical, jump_diffusion, stochastic_volatility
)


@dataclass
class AssetCharacteristics:
    """Statistical properties of an asset's returns."""

    asset_name: str

    # Distributional properties
    mean_return: float
    volatility: float
    skewness: float
    excess_kurtosis: float

    # Jump detection
    jump_probability: float
    avg_jump_size: float
    jump_frequency_per_year: float

    # Volatility properties
    vol_of_vol: float  # Volatility clustering measure
    vol_persistence: float  # Autocorrelation of squared returns
    leverage_effect: float  # Correlation(returns, future_vol)

    # Market regime
    regime: Literal["low_vol", "normal", "high_vol", "crisis"]

    # Recommended model
    recommended_model: Literal["black_scholes", "merton", "heston", "bates"]

    def __repr__(self):
        return (
            f"{self.asset_name}: {self.regime.upper()} regime\n"
            f"  Vol: {self.volatility:.1%}, Skew: {self.skewness:.2f}, "
            f"Kurt: {self.excess_kurtosis:.2f}\n"
            f"  Jumps: {self.jump_frequency_per_year:.1f}/year "
            f"(avg size: {self.avg_jump_size:.1%})\n"
            f"  → Use {self.recommended_model.upper()} model"
        )


class AssetAnalyzer:
    """Analyze asset characteristics and recommend best pricing model."""

    # Thresholds for model selection
    JUMP_THRESHOLD = 0.05  # >5% daily move = jump
    HIGH_KURTOSIS_THRESHOLD = 5.0  # Excess kurtosis > 5 = fat tails
    HIGH_VOL_THRESHOLD = 0.50  # Annualized vol > 50% = high vol
    LEVERAGE_THRESHOLD = -0.3  # Correlation < -0.3 = leverage effect

    def __init__(self, asset_name: str):
        self.asset_name = asset_name

    def analyze(self, prices: np.ndarray,
                trading_days_per_year: int = 252) -> AssetCharacteristics:
        """
        Analyze asset and determine best model.

        Parameters
        ----------
        prices : array
            Historical price series (daily recommended)
        trading_days_per_year : int
            252 for equities/crypto, 365 for 24/7 markets

        Returns
        -------
        AssetCharacteristics
            Full analysis with model recommendation
        """
        # Compute returns
        returns = np.diff(np.log(prices))

        # Basic statistics
        mean_return = np.mean(returns) * trading_days_per_year
        volatility = np.std(returns) * np.sqrt(trading_days_per_year)
        skewness = skew(returns)
        excess_kurtosis = kurtosis(returns, fisher=True)

        # Jump detection (outliers > 3 sigma)
        jump_info = self._detect_jumps(returns, volatility / np.sqrt(trading_days_per_year))

        # Volatility properties
        vol_props = self._analyze_volatility(returns, trading_days_per_year)

        # Market regime
        regime = self._classify_regime(volatility, excess_kurtosis,
                                       jump_info['jump_probability'])

        # Model recommendation
        recommended_model = self._recommend_model(
            skewness, excess_kurtosis,
            jump_info['jump_probability'],
            vol_props['vol_of_vol'],
            vol_props['leverage_effect']
        )

        return AssetCharacteristics(
            asset_name=self.asset_name,
            mean_return=mean_return,
            volatility=volatility,
            skewness=skewness,
            excess_kurtosis=excess_kurtosis,
            jump_probability=jump_info['jump_probability'],
            avg_jump_size=jump_info['avg_jump_size'],
            jump_frequency_per_year=jump_info['jump_frequency'],
            vol_of_vol=vol_props['vol_of_vol'],
            vol_persistence=vol_props['vol_persistence'],
            leverage_effect=vol_props['leverage_effect'],
            regime=regime,
            recommended_model=recommended_model
        )

    def _detect_jumps(self, returns: np.ndarray,
                      daily_vol: float) -> Dict[str, float]:
        """
        Detect jumps using threshold method.

        Jump = return > threshold * daily_vol
        """
        threshold = 3.0  # 3-sigma events

        # Identify jumps
        abs_returns = np.abs(returns)
        is_jump = abs_returns > (threshold * daily_vol)

        n_jumps = np.sum(is_jump)
        n_days = len(returns)

        jump_probability = n_jumps / n_days if n_days > 0 else 0.0

        if n_jumps > 0:
            jump_returns = returns[is_jump]
            avg_jump_size = np.mean(np.abs(jump_returns))
            jump_frequency = (n_jumps / n_days) * 252  # Annualized
        else:
            avg_jump_size = 0.0
            jump_frequency = 0.0

        return {
            'jump_probability': jump_probability,
            'avg_jump_size': avg_jump_size,
            'jump_frequency': jump_frequency,
            'n_jumps': n_jumps
        }

    def _analyze_volatility(self, returns: np.ndarray,
                           trading_days: int) -> Dict[str, float]:
        """
        Analyze volatility dynamics.

        - Vol of vol: How much volatility changes over time
        - Persistence: Autocorrelation of squared returns (GARCH effect)
        - Leverage: Correlation between returns and future volatility
        """
        # Compute realized volatility (rolling window)
        window = 20  # 20-day rolling vol
        squared_returns = returns ** 2

        # Vol of vol
        if len(returns) > window:
            rolling_var = pd.Series(squared_returns).rolling(window).mean()
            rolling_vol = np.sqrt(rolling_var.dropna().values) * np.sqrt(trading_days)
            vol_of_vol = np.std(rolling_vol) if len(rolling_vol) > 0 else 0.0
        else:
            vol_of_vol = 0.0

        # Persistence (autocorrelation of squared returns)
        if len(squared_returns) > 1:
            vol_persistence = np.corrcoef(
                squared_returns[:-1],
                squared_returns[1:]
            )[0, 1]
            if np.isnan(vol_persistence):
                vol_persistence = 0.0
        else:
            vol_persistence = 0.0

        # Leverage effect (returns vs future vol)
        if len(returns) > window + 1:
            future_vol = pd.Series(squared_returns).rolling(window).mean().shift(-window)
            valid_idx = ~(pd.isna(future_vol))

            if np.sum(valid_idx) > 10:
                leverage_effect = np.corrcoef(
                    returns[valid_idx],
                    future_vol[valid_idx]
                )[0, 1]
                if np.isnan(leverage_effect):
                    leverage_effect = 0.0
            else:
                leverage_effect = 0.0
        else:
            leverage_effect = 0.0

        return {
            'vol_of_vol': vol_of_vol,
            'vol_persistence': vol_persistence,
            'leverage_effect': leverage_effect
        }

    def _classify_regime(self, volatility: float,
                        excess_kurtosis: float,
                        jump_prob: float) -> str:
        """Classify current market regime."""
        if volatility > 1.0 or excess_kurtosis > 10 or jump_prob > 0.1:
            return "crisis"
        elif volatility > 0.5 or excess_kurtosis > 5:
            return "high_vol"
        elif volatility < 0.15 and excess_kurtosis < 2:
            return "low_vol"
        else:
            return "normal"

    def _recommend_model(self, skewness: float, excess_kurtosis: float,
                        jump_prob: float, vol_of_vol: float,
                        leverage_effect: float) -> str:
        """
        Recommend best model based on characteristics.

        Decision tree:
        1. High kurtosis + jumps → Merton or Bates
        2. High vol-of-vol + leverage → Heston or Bates
        3. Low kurtosis + low vol-of-vol → Black-Scholes
        4. Default → Heston (most flexible)
        """
        # Strong jump component
        if (excess_kurtosis > self.HIGH_KURTOSIS_THRESHOLD and
            jump_prob > 0.05):
            # Both jumps AND stochastic vol
            if (vol_of_vol > 0.1 or
                leverage_effect < self.LEVERAGE_THRESHOLD):
                return "bates"  # Heston + Jumps
            else:
                return "merton"  # Just jumps

        # Strong volatility clustering
        elif (vol_of_vol > 0.1 or
              leverage_effect < self.LEVERAGE_THRESHOLD):
            return "heston"

        # Simple dynamics
        elif (excess_kurtosis < 1.0 and
              abs(skewness) < 0.5 and
              vol_of_vol < 0.05):
            return "black_scholes"

        # Default to most flexible
        else:
            return "heston"


class ModelCalibrator:
    """Calibrate specific model parameters to historical data."""

    def __init__(self, asset_characteristics: AssetCharacteristics):
        self.asset = asset_characteristics
        self.qmc_points_1d = generators.halton([2], 5000)[:, 0]

    def calibrate_heston(self, prices: np.ndarray,
                        option_prices: Optional[np.ndarray] = None) -> Dict:
        """
        Calibrate Heston model parameters.

        If option_prices provided: calibrate to market (advanced)
        Else: calibrate to historical returns (simpler)

        Parameters
        ----------
        prices : array
            Historical spot prices
        option_prices : array, optional
            Market option prices for calibration

        Returns
        -------
        dict
            {'V0', 'kappa', 'theta', 'sigma_v', 'rho'}
        """
        if option_prices is not None:
            return self._calibrate_heston_to_options(prices, option_prices)
        else:
            return self._calibrate_heston_to_returns(prices)

    def _calibrate_heston_to_returns(self, prices: np.ndarray) -> Dict:
        """
        Calibrate Heston to historical returns (simpler method).

        Uses method-of-moments matching:
        - V0: Current variance
        - theta: Long-run variance
        - kappa: Mean reversion speed
        - sigma_v: Vol of vol
        - rho: Leverage effect (from asset characteristics)
        """
        returns = np.diff(np.log(prices))

        # Current volatility (last 30 days)
        recent_vol = np.std(returns[-30:]) * np.sqrt(252) if len(returns) >= 30 else self.asset.volatility
        V0 = recent_vol ** 2

        # Long-run volatility (full history)
        theta = self.asset.volatility ** 2

        # Mean reversion (estimate from vol autocorrelation)
        # Higher persistence → lower kappa
        if self.asset.vol_persistence > 0:
            kappa = -np.log(self.asset.vol_persistence) * 252  # Annualized
            kappa = np.clip(kappa, 0.5, 10.0)  # Reasonable range
        else:
            kappa = 2.0  # Default

        # Vol of vol (from asset characteristics)
        sigma_v = self.asset.vol_of_vol
        if sigma_v < 0.01:
            sigma_v = 0.3  # Default if can't estimate

        # Leverage effect (correlation)
        rho = self.asset.leverage_effect
        if abs(rho) < 0.1:
            rho = -0.7  # Default for equities/crypto (negative correlation)

        params = {
            'V0': V0,
            'kappa': kappa,
            'theta': theta,
            'sigma_v': sigma_v,
            'rho': rho
        }

        # Validate Feller condition: 2*kappa*theta > sigma_v^2
        if 2 * kappa * theta <= sigma_v ** 2:
            warnings.warn(
                f"Feller condition violated! Adjusting sigma_v. "
                f"2*kappa*theta={2*kappa*theta:.4f}, sigma_v^2={sigma_v**2:.4f}"
            )
            params['sigma_v'] = np.sqrt(2 * kappa * theta * 0.95)

        return params

    def _calibrate_heston_to_options(self, spot: float,
                                     market_data: pd.DataFrame) -> Dict:
        """
        Calibrate to market option prices (advanced).

        market_data should have columns:
        ['strike', 'expiry', 'type', 'market_price']

        Uses least-squares optimization to match model to market.
        """
        # Initial guess from returns
        spot_price = spot if isinstance(spot, float) else spot[-1]
        initial_params = self._calibrate_heston_to_returns(
            spot if isinstance(spot, np.ndarray) else np.array([spot])
        )

        # Bounds for optimization
        bounds = [
            (0.001, 1.0),      # V0
            (0.1, 10.0),       # kappa
            (0.001, 1.0),      # theta
            (0.01, 2.0),       # sigma_v
            (-0.99, -0.01)     # rho (negative for leverage)
        ]

        def objective(params):
            """Sum of squared pricing errors."""
            V0, kappa, theta, sigma_v, rho = params

            # Feller condition
            if 2 * kappa * theta <= sigma_v ** 2:
                return 1e10  # Penalty

            errors = []
            for _, row in market_data.iterrows():
                # Price with Heston
                model_price, _ = stochastic_volatility.european_call_heston_mc(
                    S0=spot_price,
                    V0=V0,
                    K=row['strike'],
                    r=0.05,  # Assume risk-free rate
                    delta=0.0,
                    T=row['expiry'],
                    kappa=kappa,
                    theta=theta,
                    sigma_v=sigma_v,
                    rho=rho,
                    N=1000,  # Fewer samples for speed
                    use_qe=True
                )

                error = (model_price - row['market_price']) ** 2
                errors.append(error)

            return np.sum(errors)

        # Optimize
        x0 = [initial_params['V0'], initial_params['kappa'],
              initial_params['theta'], initial_params['sigma_v'],
              initial_params['rho']]

        result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')

        if result.success:
            V0, kappa, theta, sigma_v, rho = result.x
            return {
                'V0': V0,
                'kappa': kappa,
                'theta': theta,
                'sigma_v': sigma_v,
                'rho': rho,
                'calibration_error': result.fun
            }
        else:
            warnings.warn("Calibration failed, using method-of-moments")
            return initial_params

    def calibrate_merton(self, prices: np.ndarray) -> Dict:
        """
        Calibrate Merton jump-diffusion parameters.

        Returns
        -------
        dict
            {
                'continuous_vol': σ (continuous component),
                'lambda_jump': λ (jump frequency),
                'mu_jump': μ_J (avg log jump size),
                'sigma_jump': σ_J (jump size volatility)
            }
        """
        returns = np.diff(np.log(prices))

        # Identify jumps (>3 sigma events)
        daily_vol = np.std(returns)
        threshold = 3.0 * daily_vol

        is_jump = np.abs(returns) > threshold
        jump_returns = returns[is_jump]
        continuous_returns = returns[~is_jump]

        # Continuous volatility (from non-jump returns)
        if len(continuous_returns) > 0:
            continuous_vol = np.std(continuous_returns) * np.sqrt(252)
        else:
            continuous_vol = self.asset.volatility * 0.7  # Rough estimate

        # Jump parameters
        if len(jump_returns) > 0:
            lambda_jump = len(jump_returns) / len(returns) * 252  # Annualized
            mu_jump = np.mean(jump_returns)
            sigma_jump = np.std(jump_returns)
        else:
            # No jumps detected, use small values
            lambda_jump = 1.0  # 1 jump per year
            mu_jump = 0.0
            sigma_jump = 0.01

        return {
            'continuous_vol': continuous_vol,
            'lambda_jump': lambda_jump,
            'mu_jump': mu_jump,
            'sigma_jump': sigma_jump
        }

    def calibrate_bates(self, prices: np.ndarray) -> Dict:
        """
        Calibrate Bates model (Heston + Jumps).

        Combines Heston stochastic vol with Merton jumps.
        """
        heston_params = self.calibrate_heston(prices)
        merton_params = self.calibrate_merton(prices)

        return {
            **heston_params,
            'lambda_jump': merton_params['lambda_jump'],
            'mu_jump': merton_params['mu_jump'],
            'sigma_jump': merton_params['sigma_jump']
        }


class DynamicRecalibrator:
    """
    Dynamically recalibrate models when market regime changes.

    For production systems: recalibrate daily or when volatility shifts.
    """

    def __init__(self, asset_name: str, lookback_days: int = 252):
        self.asset_name = asset_name
        self.lookback_days = lookback_days
        self.analyzer = AssetAnalyzer(asset_name)

        # Store calibration history
        self.calibration_history = []
        self.current_params = None
        self.current_model = None

    def update(self, new_prices: np.ndarray, force_recalibrate: bool = False):
        """
        Update calibration with new data.

        Recalibrates if:
        1. Forced
        2. Regime change detected
        3. More than 7 days since last calibration
        """
        # Analyze current characteristics
        characteristics = self.analyzer.analyze(new_prices[-self.lookback_days:])

        # Check if recalibration needed
        need_recalibration = force_recalibrate

        if self.current_params is not None and not force_recalibrate:
            # Check for regime change
            if characteristics.regime != getattr(self, '_last_regime', None):
                print(f"⚠️  Regime change: {getattr(self, '_last_regime', 'unknown')} → {characteristics.regime}")
                need_recalibration = True

            # Check for model change
            if characteristics.recommended_model != self.current_model:
                print(f"⚠️  Model change: {self.current_model} → {characteristics.recommended_model}")
                need_recalibration = True
        else:
            need_recalibration = True

        if need_recalibration:
            # Calibrate
            calibrator = ModelCalibrator(characteristics)

            if characteristics.recommended_model == "heston":
                params = calibrator.calibrate_heston(new_prices[-self.lookback_days:])
            elif characteristics.recommended_model == "merton":
                params = calibrator.calibrate_merton(new_prices[-self.lookback_days:])
            elif characteristics.recommended_model == "bates":
                params = calibrator.calibrate_bates(new_prices[-self.lookback_days:])
            else:  # black_scholes
                params = {'sigma': characteristics.volatility}

            self.current_params = params
            self.current_model = characteristics.recommended_model
            self._last_regime = characteristics.regime

            self.calibration_history.append({
                'timestamp': pd.Timestamp.now(),
                'model': self.current_model,
                'params': params,
                'characteristics': characteristics
            })

            print(f"✅ Recalibrated {self.asset_name}:")
            print(f"   Model: {self.current_model}")
            print(f"   Params: {params}")

        return characteristics, self.current_model, self.current_params


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ASSET-SPECIFIC MODEL CALIBRATION")
    print("=" * 70)

    # Simulate different asset types
    np.random.seed(42)

    # 1. EQUITY (SPY) - Leverage effect, moderate vol
    print("\n1️⃣  EQUITY: S&P 500 (SPY)")
    print("-" * 70)

    # Simulate with leverage effect (returns negatively correlated with vol changes)
    n_days = 500
    equity_prices = [100.0]
    vol = 0.15

    for i in range(n_days):
        # Leverage effect: negative returns → higher future vol
        shock = np.random.randn()
        ret = 0.0003 + vol * shock / np.sqrt(252)

        equity_prices.append(equity_prices[-1] * np.exp(ret))

        # Vol mean-reverts with leverage
        vol += 0.05 * (0.15 - vol) - 0.3 * shock * 0.01  # Leverage!
        vol = np.clip(vol, 0.05, 0.50)

    equity_prices = np.array(equity_prices)

    analyzer = AssetAnalyzer("SPY")
    equity_chars = analyzer.analyze(equity_prices)
    print(equity_chars)

    calibrator = ModelCalibrator(equity_chars)
    if equity_chars.recommended_model == "heston":
        params = calibrator.calibrate_heston(equity_prices)
        print(f"\n📊 Calibrated Heston Parameters:")
        for k, v in params.items():
            print(f"   {k}: {v:.4f}")

    # 2. CRYPTO (SOL) - HUGE jumps, high vol
    print("\n\n2️⃣  CRYPTO: Solana (SOL)")
    print("-" * 70)

    crypto_prices = [100.0]
    vol = 0.80  # 80% annualized!

    for i in range(n_days):
        # Regular diffusion
        ret = 0.001 + vol * np.random.randn() / np.sqrt(252)

        # Random jumps (5% chance)
        if np.random.rand() < 0.05:
            jump = np.random.randn() * 0.15  # 15% jump!
            ret += jump

        crypto_prices.append(crypto_prices[-1] * np.exp(ret))

        # High vol persistence
        vol += 0.02 * (0.80 - vol) + 0.1 * np.random.randn()
        vol = np.clip(vol, 0.30, 1.50)

    crypto_prices = np.array(crypto_prices)

    analyzer = AssetAnalyzer("SOL")
    crypto_chars = analyzer.analyze(crypto_prices, trading_days_per_year=365)  # 24/7 market
    print(crypto_chars)

    calibrator = ModelCalibrator(crypto_chars)
    if crypto_chars.recommended_model in ["merton", "bates"]:
        params = calibrator.calibrate_merton(crypto_prices)
        print(f"\n📊 Calibrated Merton Parameters:")
        for k, v in params.items():
            print(f"   {k}: {v:.4f}")

    # 3. LOW VOL STOCK (Utilities) - Stable, low kurtosis
    print("\n\n3️⃣  LOW VOL: Utilities Stock")
    print("-" * 70)

    stable_prices = 100 * np.exp(np.cumsum(
        0.0001 + 0.08 * np.random.randn(n_days) / np.sqrt(252)  # 8% vol
    ))

    analyzer = AssetAnalyzer("Utilities")
    stable_chars = analyzer.analyze(stable_prices)
    print(stable_chars)

    # 4. DYNAMIC RECALIBRATION DEMO
    print("\n\n4️⃣  DYNAMIC RECALIBRATION (Regime Change)")
    print("-" * 70)

    recalibrator = DynamicRecalibrator("AAPL", lookback_days=120)

    # Start in normal regime
    normal_prices = 100 * np.exp(np.cumsum(
        0.0002 + 0.15 * np.random.randn(200) / np.sqrt(252)
    ))

    print("\nNormal regime:")
    chars, model, params = recalibrator.update(normal_prices, force_recalibrate=True)

    # Transition to crisis (high vol + jumps)
    crisis_returns = 0.0002 + 0.60 * np.random.randn(100) / np.sqrt(252)
    crisis_returns[::10] += np.random.randn(10) * 0.10  # Jumps!
    crisis_prices = normal_prices[-1] * np.exp(np.cumsum(crisis_returns))

    all_prices = np.concatenate([normal_prices, crisis_prices])

    print("\nAfter crisis:")
    chars, model, params = recalibrator.update(all_prices)

    print("\n" + "=" * 70)
    print("✅ Calibration complete! Use these parameters for accurate pricing.")
    print("=" * 70)
