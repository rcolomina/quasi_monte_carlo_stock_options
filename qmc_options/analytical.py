"""
Analytical formulas for option pricing and Greeks.

This module implements closed-form solutions including:
- Black-Scholes formula for European options
- Margrabe formula for spread options
- Greeks (Delta, Gamma, Vega, Theta, Rho)
"""

import numpy as np
from scipy import stats


def d1(S0: float, K: float, r: float, delta: float, sigma: float, T: float) -> float:
    """
    Calculate d1 parameter for Black-Scholes formula.

    Parameters
    ----------
    S0 : float
        Current stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    T : float
        Time to maturity

    Returns
    -------
    float
        d1 parameter
    """
    return (np.log(S0 / K) + (r - delta + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))


def d2(S0: float, K: float, r: float, delta: float, sigma: float, T: float) -> float:
    """Calculate d2 parameter for Black-Scholes formula."""
    return d1(S0, K, r, delta, sigma, T) - sigma * np.sqrt(T)


def black_scholes_call(S0: float, K: float, r: float, delta: float,
                       sigma: float, T: float) -> float:
    """
    Black-Scholes formula for European call option.

    Parameters
    ----------
    S0 : float
        Current stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    T : float
        Time to maturity

    Returns
    -------
    float
        Call option price
    """
    d1_val = d1(S0, K, r, delta, sigma, T)
    d2_val = d2(S0, K, r, delta, sigma, T)

    call_price = (S0 * np.exp(-delta * T) * stats.norm.cdf(d1_val) -
                  K * np.exp(-r * T) * stats.norm.cdf(d2_val))

    return call_price


def black_scholes_put(S0: float, K: float, r: float, delta: float,
                      sigma: float, T: float) -> float:
    """
    Black-Scholes formula for European put option.

    Uses put-call parity.

    Parameters
    ----------
    S0 : float
        Current stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    T : float
        Time to maturity

    Returns
    -------
    float
        Put option price
    """
    d1_val = d1(S0, K, r, delta, sigma, T)
    d2_val = d2(S0, K, r, delta, sigma, T)

    put_price = (K * np.exp(-r * T) * stats.norm.cdf(-d2_val) -
                 S0 * np.exp(-delta * T) * stats.norm.cdf(-d1_val))

    return put_price


def margrabe_formula(S10: float, S20: float, delta1: float, delta2: float,
                     sigma1: float, sigma2: float, rho12: float, T: float) -> float:
    """
    Margrabe formula for spread option with K=0.

    Prices an option with payoff max(w1*S1 - w2*S2, 0) where w1=w2=1.

    Parameters
    ----------
    S10 : float
        Initial price of first underlying
    S20 : float
        Initial price of second underlying
    delta1 : float
        Dividend yield of first underlying
    delta2 : float
        Dividend yield of second underlying
    sigma1 : float
        Volatility of first underlying
    sigma2 : float
        Volatility of second underlying
    rho12 : float
        Correlation between underlyings
    T : float
        Time to maturity

    Returns
    -------
    float
        Spread option price
    """
    sigma = np.sqrt(sigma1 ** 2 + sigma2 ** 2 - 2 * sigma1 * sigma2 * rho12)

    d2_val = (np.log(S20 / S10) + (delta1 - delta2 + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d1_val = d2_val - sigma * np.sqrt(T)

    price = (np.exp(-delta2 * T) * S20 * stats.norm.cdf(d2_val) -
             np.exp(-delta1 * T) * S10 * stats.norm.cdf(d1_val))

    return price


# Greeks for European Call Options

def call_delta(S0: float, K: float, r: float, delta: float,
               sigma: float, T: float) -> float:
    """
    Delta of European call option: ∂C/∂S.

    Parameters
    ----------
    S0 : float
        Current stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    T : float
        Time to maturity

    Returns
    -------
    float
        Delta
    """
    d1_val = d1(S0, K, r, delta, sigma, T)
    return np.exp(-delta * T) * stats.norm.cdf(d1_val)


def call_gamma(S0: float, K: float, r: float, delta: float,
               sigma: float, T: float) -> float:
    """
    Gamma of European call option: ∂²C/∂S².

    Parameters
    ----------
    S0 : float
        Current stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    T : float
        Time to maturity

    Returns
    -------
    float
        Gamma
    """
    d1_val = d1(S0, K, r, delta, sigma, T)
    return np.exp(-delta * T) * stats.norm.pdf(d1_val) / (sigma * S0 * np.sqrt(T))


def call_vega(S0: float, K: float, r: float, delta: float,
              sigma: float, T: float) -> float:
    """
    Vega of European call option: ∂C/∂σ.

    Parameters
    ----------
    S0 : float
        Current stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    T : float
        Time to maturity

    Returns
    -------
    float
        Vega
    """
    d1_val = d1(S0, K, r, delta, sigma, T)
    return np.sqrt(T) * S0 * np.exp(-delta * T) * stats.norm.pdf(d1_val)


def call_theta(S0: float, K: float, r: float, delta: float,
               sigma: float, T: float) -> float:
    """
    Theta of European call option: -∂C/∂T.

    Parameters
    ----------
    S0 : float
        Current stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    T : float
        Time to maturity

    Returns
    -------
    float
        Theta
    """
    d1_val = d1(S0, K, r, delta, sigma, T)
    d2_val = d2(S0, K, r, delta, sigma, T)

    term1 = -sigma * np.exp(-delta * T) * S0 * stats.norm.pdf(d1_val) / (2 * np.sqrt(T))
    term2 = delta * np.exp(-delta * T) * S0 * stats.norm.cdf(d1_val)
    term3 = -r * K * np.exp(-r * T) * stats.norm.cdf(d2_val)

    return term1 + term2 + term3


def call_rho(S0: float, K: float, r: float, delta: float,
             sigma: float, T: float) -> float:
    """
    Rho of European call option: ∂C/∂r.

    Parameters
    ----------
    S0 : float
        Current stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    T : float
        Time to maturity

    Returns
    -------
    float
        Rho
    """
    d2_val = d2(S0, K, r, delta, sigma, T)
    return K * T * np.exp(-r * T) * stats.norm.cdf(d2_val)
