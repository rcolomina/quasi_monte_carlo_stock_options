"""
Tests for analytical formulas.
"""

import pytest
import numpy as np
from qmc_options import analytical


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


def test_black_scholes_call(option_params):
    """Test Black-Scholes call pricing."""
    price = analytical.black_scholes_call(**option_params)

    # Price should be positive
    assert price > 0

    # For ATM call with positive rates, price should be reasonable
    assert 5 < price < 20


def test_black_scholes_put(option_params):
    """Test Black-Scholes put pricing."""
    price = analytical.black_scholes_put(**option_params)

    # Price should be positive
    assert price > 0


def test_put_call_parity(option_params):
    """Test put-call parity relationship."""
    call = analytical.black_scholes_call(**option_params)
    put = analytical.black_scholes_put(**option_params)

    S0 = option_params['S0']
    K = option_params['K']
    r = option_params['r']
    delta = option_params['delta']
    T = option_params['T']

    # Put-Call Parity: C - P = S*e^(-δT) - K*e^(-rT)
    lhs = call - put
    rhs = S0 * np.exp(-delta * T) - K * np.exp(-r * T)

    assert np.isclose(lhs, rhs, rtol=1e-10)


def test_margrabe_formula():
    """Test Margrabe formula for spread options."""
    price = analytical.margrabe_formula(
        S10=100, S20=110,
        delta1=0.05, delta2=0.05,
        sigma1=0.3, sigma2=0.2,
        rho12=0.8, T=1.0
    )

    # Price should be positive
    assert price > 0


def test_call_delta(option_params):
    """Test call delta calculation."""
    delta = analytical.call_delta(**option_params)

    # Delta should be between 0 and 1 for call
    assert 0 < delta < 1


def test_call_gamma(option_params):
    """Test call gamma calculation."""
    gamma = analytical.call_gamma(**option_params)

    # Gamma should be positive
    assert gamma > 0


def test_call_vega(option_params):
    """Test call vega calculation."""
    vega = analytical.call_vega(**option_params)

    # Vega should be positive
    assert vega > 0


def test_call_theta(option_params):
    """Test call theta calculation."""
    theta = analytical.call_theta(**option_params)

    # Theta is typically negative for long calls
    # (but can be positive with dividends)
    assert isinstance(theta, float)


def test_call_rho(option_params):
    """Test call rho calculation."""
    rho = analytical.call_rho(**option_params)

    # Rho should be positive for call
    assert rho > 0


def test_itm_call_delta():
    """Test delta for deep ITM call approaches 1."""
    params = {
        'S0': 150.0,  # Deep ITM
        'K': 100.0,
        'r': 0.05,
        'delta': 0.02,
        'sigma': 0.2,
        'T': 1.0
    }
    delta = analytical.call_delta(**params)

    # Deep ITM call delta should be close to 1
    assert delta > 0.9


def test_otm_call_delta():
    """Test delta for deep OTM call approaches 0."""
    params = {
        'S0': 50.0,  # Deep OTM
        'K': 100.0,
        'r': 0.05,
        'delta': 0.02,
        'sigma': 0.2,
        'T': 1.0
    }
    delta = analytical.call_delta(**params)

    # Deep OTM call delta should be close to 0
    assert delta < 0.1
