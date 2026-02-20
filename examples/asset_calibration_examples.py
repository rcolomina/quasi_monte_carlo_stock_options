"""
Practical examples of asset-specific calibration.

Run this to see how different assets require different models and parameters.
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmc_options.calibration import AssetAnalyzer, ModelCalibrator, DynamicRecalibrator
from qmc_options.market_data import calibrate_asset_from_ticker
from qmc_options import stochastic_volatility, jump_diffusion, generators


def example_1_equity_calibration():
    """
    Example 1: Calibrate a blue-chip equity (Apple).

    Expected: Heston model with moderate vol, negative leverage effect.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 1: EQUITY CALIBRATION (AAPL)")
    print("=" * 80)

    try:
        result = calibrate_asset_from_ticker("AAPL", lookback_days=252)

        print(f"\n📊 Results:")
        print(f"   Current price: ${result['current_price']:.2f}")
        print(f"   Volatility: {result['characteristics'].volatility:.2%}")
        print(f"   Skewness: {result['characteristics'].skewness:.2f}")
        print(f"   Excess kurtosis: {result['characteristics'].excess_kurtosis:.2f}")
        print(f"   Leverage effect: {result['characteristics'].leverage_effect:.2f}")
        print(f"   Recommended model: {result['model'].upper()}")

        # Price an ATM call option
        if result['model'] == 'heston':
            params = result['parameters']
            S0 = result['current_price']

            print(f"\n💰 Pricing 30-day ATM call option...")
            call_price, std_err = stochastic_volatility.european_call_heston_mc(
                S0=S0,
                V0=params['V0'],
                K=S0,  # ATM
                r=0.05,
                delta=0.02,  # 2% dividend yield
                T=30/252,
                kappa=params['kappa'],
                theta=params['theta'],
                sigma_v=params['sigma_v'],
                rho=params['rho'],
                N=5000
            )

            print(f"   Call price: ${call_price:.2f} ± {std_err:.2f}")
            print(f"   As % of stock: {call_price/S0:.2%}")

        return result

    except Exception as e:
        print(f"⚠️  Could not calibrate AAPL: {e}")
        print("Make sure yfinance is installed: pip install yfinance")
        return None


def example_2_crypto_calibration():
    """
    Example 2: Calibrate a cryptocurrency (Bitcoin).

    Expected: Merton or Bates model with high vol, frequent jumps.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: CRYPTO CALIBRATION (Bitcoin)")
    print("=" * 80)

    try:
        result = calibrate_asset_from_ticker("BTCUSDT",
                                             lookback_days=180,
                                             asset_type="crypto_binance")

        print(f"\n📊 Results:")
        print(f"   Current price: ${result['current_price']:.2f}")
        print(f"   Volatility: {result['characteristics'].volatility:.2%}")
        print(f"   Jump frequency: {result['characteristics'].jump_frequency_per_year:.1f}/year")
        print(f"   Avg jump size: {result['characteristics'].avg_jump_size:.2%}")
        print(f"   Recommended model: {result['model'].upper()}")

        # Price with jump model
        if result['model'] in ['merton', 'bates']:
            params = result['parameters']
            S0 = result['current_price']

            print(f"\n💰 Pricing 7-day ATM call option (with jumps)...")

            qmc_points = generators.halton([2], 5000)[:, 0]

            call_price, std_err = jump_diffusion.european_call_merton_mc(
                S0=S0,
                K=S0,  # ATM
                r=0.05,
                delta=0.0,  # No dividends
                sigma=params['continuous_vol'],
                T=7/365,  # 7 days, 365 days/year for crypto
                lambda_jump=params['lambda_jump'],
                mu_jump=params['mu_jump'],
                sigma_jump=params['sigma_jump'],
                points=qmc_points
            )

            print(f"   Call price: ${call_price:.2f} ± {std_err:.2f}")
            print(f"   As % of Bitcoin: {call_price/S0:.2%}")

            # Compare to no-jump pricing
            from qmc_options import analytical
            bs_price = analytical.european_call(
                S0=S0, K=S0, r=0.05, delta=0.0,
                sigma=result['characteristics'].volatility,
                T=7/365
            )
            print(f"\n   Comparison:")
            print(f"   Black-Scholes (no jumps): ${bs_price:.2f}")
            print(f"   Merton (with jumps): ${call_price:.2f}")
            print(f"   Jump premium: ${call_price - bs_price:.2f} ({(call_price/bs_price - 1):.1%})")

        return result

    except Exception as e:
        print(f"⚠️  Could not calibrate Bitcoin: {e}")
        print("Make sure you have internet connection for Binance API")
        return None


def example_3_simulated_assets():
    """
    Example 3: Analyze simulated assets with known properties.

    This validates that our calibration correctly identifies asset characteristics.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: SIMULATED ASSETS (Validation)")
    print("=" * 80)

    np.random.seed(42)

    # 3a: Simulate stable asset (should recommend Black-Scholes)
    print("\n3a. Stable Asset (Low vol, no jumps)")
    print("-" * 80)

    stable_prices = 100 * np.exp(np.cumsum(
        0.0001 + 0.10 * np.random.randn(500) / np.sqrt(252)  # 10% vol
    ))

    analyzer = AssetAnalyzer("Stable Corp")
    chars = analyzer.analyze(stable_prices)
    print(chars)

    # 3b: Simulate jump asset (should recommend Merton)
    print("\n3b. Jumpy Asset (Frequent jumps)")
    print("-" * 80)

    jumpy_prices = [100.0]
    for i in range(500):
        ret = 0.0001 + 0.20 * np.random.randn() / np.sqrt(252)

        # Add jumps (10% chance)
        if np.random.rand() < 0.10:
            ret += np.random.randn() * 0.08  # 8% jump

        jumpy_prices.append(jumpy_prices[-1] * np.exp(ret))

    jumpy_prices = np.array(jumpy_prices)

    analyzer = AssetAnalyzer("Jumpy Inc")
    chars = analyzer.analyze(jumpy_prices)
    print(chars)

    # 3c: Simulate leverage effect asset (should recommend Heston)
    print("\n3c. Leverage Effect Asset (Vol increases with negative returns)")
    print("-" * 80)

    leverage_prices = [100.0]
    vol = 0.15

    for i in range(500):
        shock = np.random.randn()
        ret = 0.0002 + vol * shock / np.sqrt(252)

        leverage_prices.append(leverage_prices[-1] * np.exp(ret))

        # Leverage effect: negative returns → higher vol
        vol += 0.05 * (0.15 - vol) - 0.5 * shock * 0.01
        vol = np.clip(vol, 0.05, 0.50)

    leverage_prices = np.array(leverage_prices)

    analyzer = AssetAnalyzer("Leverage Corp")
    chars = analyzer.analyze(leverage_prices)
    print(chars)


def example_4_dynamic_recalibration():
    """
    Example 4: Dynamic recalibration when regime changes.

    Simulates a regime shift (normal → crisis) and shows recalibration.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: DYNAMIC RECALIBRATION (Regime Change)")
    print("=" * 80)

    np.random.seed(42)

    # Create recalibrator
    recalibrator = DynamicRecalibrator("Test Asset", lookback_days=120)

    # Phase 1: Normal regime
    print("\nPhase 1: Normal Regime")
    print("-" * 80)

    normal_prices = 100 * np.exp(np.cumsum(
        0.0002 + 0.18 * np.random.randn(200) / np.sqrt(252)
    ))

    chars1, model1, params1 = recalibrator.update(normal_prices, force_recalibrate=True)

    print(f"Volatility: {chars1.volatility:.2%}")
    print(f"Regime: {chars1.regime}")
    print(f"Model: {model1}")

    # Phase 2: Crisis (high vol + jumps)
    print("\nPhase 2: CRISIS (regime shift)")
    print("-" * 80)

    crisis_returns = 0.0002 + 0.70 * np.random.randn(100) / np.sqrt(252)
    # Add jumps
    crisis_returns[::8] += np.random.randn(13) * 0.12  # Jumps every ~8 days

    crisis_prices = normal_prices[-1] * np.exp(np.cumsum(crisis_returns))

    all_prices = np.concatenate([normal_prices, crisis_prices])

    chars2, model2, params2 = recalibrator.update(all_prices)

    print(f"Volatility: {chars2.volatility:.2%}")
    print(f"Regime: {chars2.regime}")
    print(f"Model: {model2}")

    if model1 != model2:
        print(f"\n⚠️  MODEL CHANGED: {model1} → {model2}")
        print("This is expected during regime shifts!")

    # Phase 3: Return to normal
    print("\nPhase 3: Recovery (back to normal)")
    print("-" * 80)

    recovery_prices = crisis_prices[-1] * np.exp(np.cumsum(
        0.0003 + 0.20 * np.random.randn(150) / np.sqrt(252)
    ))

    all_prices = np.concatenate([all_prices, recovery_prices])

    chars3, model3, params3 = recalibrator.update(all_prices)

    print(f"Volatility: {chars3.volatility:.2%}")
    print(f"Regime: {chars3.regime}")
    print(f"Model: {model3}")


def example_5_model_comparison():
    """
    Example 5: Compare pricing across different models.

    Shows how much model choice affects option prices.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: MODEL COMPARISON")
    print("=" * 80)

    from qmc_options import analytical

    S0 = 100.0
    K = 105.0  # 5% OTM
    r = 0.05
    delta = 0.0
    T = 30/252
    base_vol = 0.30

    print(f"\nPricing 30-day call, Strike ${K}, Spot ${S0}")
    print("-" * 80)

    # 1. Black-Scholes
    bs_price = analytical.european_call(S0, K, r, delta, base_vol, T)
    print(f"1. Black-Scholes: ${bs_price:.2f}")

    # 2. Heston
    heston_price, _ = stochastic_volatility.european_call_heston_mc(
        S0=S0, V0=base_vol**2, K=K, r=r, delta=delta, T=T,
        kappa=2.0, theta=base_vol**2, sigma_v=0.3, rho=-0.7,
        N=5000
    )
    print(f"2. Heston: ${heston_price:.2f}")

    # 3. Merton (with jumps)
    qmc_points = generators.halton([2], 5000)[:, 0]
    merton_price, _ = jump_diffusion.european_call_merton_mc(
        S0=S0, K=K, r=r, delta=delta, sigma=base_vol, T=T,
        lambda_jump=5.0,  # 5 jumps/year
        mu_jump=-0.02,    # Avg -2% jump
        sigma_jump=0.10,  # 10% jump volatility
        points=qmc_points
    )
    print(f"3. Merton (jumps): ${merton_price:.2f}")

    # Show differences
    print(f"\n📊 Price Differences:")
    print(f"   Heston vs BS: {(heston_price/bs_price - 1):.1%}")
    print(f"   Merton vs BS: {(merton_price/bs_price - 1):.1%}")

    print(f"\n💡 Insight: Jump models typically price higher (tail risk premium)")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("ASSET-SPECIFIC CALIBRATION EXAMPLES")
    print("=" * 80)
    print("\nThese examples show how to:")
    print("  1. Calibrate models to real market data")
    print("  2. Select the right model for each asset type")
    print("  3. Dynamically recalibrate when regimes change")
    print("  4. Compare pricing across different models")

    # Run examples
    example_1_equity_calibration()
    example_2_crypto_calibration()
    example_3_simulated_assets()
    example_4_dynamic_recalibration()
    example_5_model_comparison()

    print("\n" + "=" * 80)
    print("✅ ALL EXAMPLES COMPLETE")
    print("=" * 80)
    print("\n💡 Key Takeaways:")
    print("   1. Different assets need different models")
    print("   2. High kurtosis + jumps → Use Merton or Bates")
    print("   3. Leverage effect + vol clustering → Use Heston")
    print("   4. Recalibrate when volatility regime changes")
    print("   5. Model choice can affect prices by 10-30%")
    print("\n📚 See docs/ASSET_CALIBRATION_GUIDE.md for full details")


if __name__ == "__main__":
    main()
