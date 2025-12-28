"""
Tests for option pricing functions.
"""

import pytest
import numpy as np
from qmc_options import pricing, analytical, generators


@pytest.fixture
def option_params():
    """Standard option parameters for testing."""
    return {
        'S0': 100.0,
        'K': 100.0,
        'r': 0.05,
        'delta': 0.02,
        'sigma': 0.2,
        'T': 1.0
    }


def test_european_call_mc(option_params):
    """Test European call pricing with MC."""
    # Generate random points
    np.random.seed(42)
    points = np.random.rand(10000)

    price = pricing.european_call_mc(
        points=points,
        **option_params
    )

    # Compare with Black-Scholes
    bs_price = analytical.black_scholes_call(**option_params)

    # Should be within 5% of analytical price
    rel_error = abs(price - bs_price) / bs_price
    assert rel_error < 0.05


def test_spread_option_zero_strike():
    """Test spread option with K=0 against Margrabe formula."""
    # Generate QMC points
    N = 5000
    glp = generators.good_lattice_points_nd(N, 2)

    mc_price = pricing.spread_option(
        points=glp,
        w1=1.0, w2=1.0,
        r=0.05, K=0.0,
        S10=100, S20=110,
        delta1=0.05, delta2=0.05,
        sigma1=0.3, sigma2=0.2,
        rho12=0.8, T=1.0
    )

    # Margrabe formula (exact for K=0)
    margrabe_price = analytical.margrabe_formula(
        S10=100, S20=110,
        delta1=0.05, delta2=0.05,
        sigma1=0.3, sigma2=0.2,
        rho12=0.8, T=1.0
    )

    # Should be close to Margrabe price
    rel_error = abs(mc_price - margrabe_price) / margrabe_price
    assert rel_error < 0.10  # Within 10%


def test_asian_call(option_params):
    """Test Asian call option pricing."""
    # Generate QMC points
    m = 12  # Monthly monitoring
    N = 1000
    points = generators.halton([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37], N)

    price = pricing.asian_call(
        m=m,
        points=points,
        **option_params
    )

    # Asian option should be cheaper than European
    euro_price = analytical.black_scholes_call(**option_params)
    assert price < euro_price
    assert price > 0


def test_lookback_call(option_params):
    """Test lookback call option pricing."""
    # Generate QMC points
    m = 12
    N = 1000
    points = generators.halton([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37], N)

    price = pricing.lookback_call(
        points=points,
        **option_params
    )

    # Lookback should be more expensive than European
    euro_price = analytical.black_scholes_call(**option_params)
    assert price > euro_price


def test_lookback_put(option_params):
    """Test lookback put option pricing."""
    # Generate QMC points
    m = 12
    N = 1000
    points = generators.halton([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37], N)

    price = pricing.lookback_put(
        points=points,
        **option_params
    )

    # Price should be positive
    assert price > 0


def test_mc_qmc_comparison_european():
    """Compare MC and QMC for European option."""
    params = {
        'S0': 100.0,
        'K': 100.0,
        'r': 0.05,
        'delta': 0.02,
        'sigma': 0.2,
        'T': 1.0
    }

    N = 5000

    # MC with random points
    np.random.seed(42)
    mc_points = np.random.rand(N)
    mc_price = pricing.european_call_mc(points=mc_points, **params)

    # QMC with Halton sequence
    qmc_points = generators.halton([2], N)[:, 0]
    qmc_price = pricing.european_call_mc(points=qmc_points, **params)

    # Both should be close to analytical
    bs_price = analytical.black_scholes_call(**params)

    mc_error = abs(mc_price - bs_price) / bs_price
    qmc_error = abs(qmc_price - bs_price) / bs_price

    # QMC should generally have lower error
    # (though not guaranteed for single run)
    assert qmc_error < 0.10
    assert mc_error < 0.10
