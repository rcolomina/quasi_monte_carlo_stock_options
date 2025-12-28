"""
Option pricing functions using Monte Carlo and Quasi-Monte Carlo methods.

This module implements pricing for:
- European options (vanilla calls and puts)
- Spread options
- Asian options
- Lookback options
"""

import numpy as np
from scipy import stats
from .simulation import qmc_to_normal, gbm_explicit


def european_call_mc(S0: float, K: float, r: float, delta: float,
                     sigma: float, T: float, points: np.ndarray) -> float:
    """
    Price European call option using Monte Carlo/QMC.

    Parameters
    ----------
    S0 : float
        Initial stock price
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
    points : np.ndarray
        Array of points in [0,1) for MC/QMC integration

    Returns
    -------
    float
        Call option price
    """
    N = len(points)
    payoffs = np.zeros(N)

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            ST = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
            payoffs[i] = max(ST - K, 0)

    return np.exp(-r * T) * np.mean(payoffs)


def spread_option(points: np.ndarray, w1: float, w2: float, r: float, K: float,
                  S10: float, S20: float, delta1: float, delta2: float,
                  sigma1: float, sigma2: float, rho12: float, T: float,
                  periodization: int = 8) -> float:
    """
    Price spread option using QMC: max(w1*S1 - w2*S2 - K, 0).

    Uses importance sampling with conditional distribution.

    Parameters
    ----------
    points : np.ndarray
        Array of shape (N, 2) with QMC points in [0,1)^2
    w1 : float
        Weight of first underlying
    w2 : float
        Weight of second underlying
    r : float
        Risk-free interest rate
    K : float
        Strike price
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
    periodization : int, default=8
        Periodization transformation (1-8). Default 8 = identity (no transform).

    Returns
    -------
    float
        Spread option price
    """
    from .periodization import PeriodicTransform

    N = len(points)
    value = 0.0

    # Drift-adjusted means
    mu1T = np.log(S10) + (r - delta1 - 0.5 * sigma1 ** 2) * T
    mu2T = np.log(S20) + (r - delta2 - 0.5 * sigma2 ** 2) * T

    # Cholesky decomposition of covariance matrix
    c11 = sigma1 * np.sqrt(T)
    c21 = rho12 * sigma2 * np.sqrt(T)
    c22 = np.sqrt(1 - rho12 ** 2) * sigma2 * np.sqrt(T)

    for i in range(N):
        # Apply periodization transformation
        u1_raw, u2_raw = points[i, 0], points[i, 1]
        u1 = PeriodicTransform.transform(np.array([u1_raw]), periodization)[0]
        u2 = PeriodicTransform.transform(np.array([u2_raw]), periodization)[0]

        # Jacobian from periodization
        du1 = PeriodicTransform.derivative(np.array([u1_raw]), periodization)[0]
        du2 = PeriodicTransform.derivative(np.array([u2_raw]), periodization)[0]
        jacobian = du1 * du2

        if u1 > 0:  # Safety criterion
            inv_u1 = stats.norm.ppf(u1)
            h3 = c11 * inv_u1 + mu1T
            h1 = w1 * np.exp(h3)

            g = (np.log(h1 + K) - np.log(w2) - mu2T - c21 * inv_u1) / c22
            d2 = stats.norm.cdf(g)

            if (d2 + u2 * (1 - d2)) < 1:  # Safety criterion
                h5 = stats.norm.ppf(d2 + u2 * (1 - d2))
                h4 = c21 * inv_u1 + c22 * h5 + mu2T
                h2 = w2 * np.exp(h4)
                h = h2 - h1 - K
                value += (1 - d2) * h * jacobian

    return np.exp(-r * T) * value / N


def asian_call(S0: float, K: float, r: float, delta: float, sigma: float,
               m: int, T: float, points: np.ndarray) -> float:
    """
    Price arithmetic average Asian call option.

    Payoff: max(avg(S_1, ..., S_m) - K, 0)

    Parameters
    ----------
    S0 : float
        Initial stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    m : int
        Number of monitoring points
    T : float
        Time to maturity
    points : np.ndarray
        Array of shape (N, m) with QMC points in [0,1)^m

    Returns
    -------
    float
        Asian call option price
    """
    N = len(points)
    payoffs = np.zeros(N)

    for i in range(N):
        # Check if all points are positive (safety)
        if np.all(points[i, :] > 0):
            Z = qmc_to_normal(points[i, :])

            # Generate price path
            prices = np.zeros(m)
            for j in range(m):
                prices[j] = gbm_explicit(S0, r, sigma, delta, j + 1, T, Z)

            avg_price = np.mean(prices)
            payoffs[i] = max(avg_price - K, 0)

    return np.exp(-r * T) * np.mean(payoffs)


def lookback_call(S0: float, K: float, r: float, delta: float, sigma: float,
                  T: float, points: np.ndarray) -> float:
    """
    Price discrete lookback call option.

    Payoff: max(max(S_0, S_1, ..., S_m) - K, 0)

    Parameters
    ----------
    S0 : float
        Initial stock price
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
    points : np.ndarray
        Array of shape (N, m) with QMC points in [0,1)^m

    Returns
    -------
    float
        Lookback call option price
    """
    N, m = points.shape
    payoffs = np.zeros(N)
    dt = T / m

    for i in range(N):
        if np.all(points[i, :] > 0):
            Z = qmc_to_normal(points[i, :])

            # Generate price path
            prices = np.zeros(m + 1)
            prices[0] = S0

            for j in range(m):
                aux1 = np.exp((r - delta - 0.5 * sigma ** 2) * dt)
                aux2 = np.exp(sigma * np.sqrt(dt) * Z[j])
                prices[j + 1] = prices[j] * aux1 * aux2

            max_price = np.max(prices)
            payoffs[i] = max(max_price - K, 0)

    return np.exp(-r * T) * np.mean(payoffs)


def lookback_put(S0: float, K: float, r: float, delta: float, sigma: float,
                 T: float, points: np.ndarray) -> float:
    """
    Price discrete lookback put option.

    Payoff: max(K - min(S_0, S_1, ..., S_m), 0)

    Parameters
    ----------
    S0 : float
        Initial stock price
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
    points : np.ndarray
        Array of shape (N, m) with QMC points in [0,1)^m

    Returns
    -------
    float
        Lookback put option price
    """
    N, m = points.shape
    payoffs = np.zeros(N)
    dt = T / m

    for i in range(N):
        if np.all(points[i, :] > 0):
            Z = qmc_to_normal(points[i, :])

            # Generate price path
            prices = np.zeros(m + 1)
            prices[0] = S0

            for j in range(m):
                aux1 = np.exp((r - delta - 0.5 * sigma ** 2) * dt)
                aux2 = np.exp(sigma * np.sqrt(dt) * Z[j])
                prices[j + 1] = prices[j] * aux1 * aux2

            min_price = np.min(prices)
            payoffs[i] = max(K - min_price, 0)

    return np.exp(-r * T) * np.mean(payoffs)


def monte_carlo_convergence(pricer_func, points_list: list, *args, **kwargs) -> np.ndarray:
    """
    Test convergence of MC/QMC pricing with different sample sizes.

    Parameters
    ----------
    pricer_func : callable
        Pricing function to test
    points_list : list
        List of point sets with increasing sizes
    *args, **kwargs
        Additional arguments to pass to pricer_func

    Returns
    -------
    np.ndarray
        Array of prices for each point set
    """
    prices = np.zeros(len(points_list))

    for i, points in enumerate(points_list):
        prices[i] = pricer_func(points, *args, **kwargs)

    return prices
