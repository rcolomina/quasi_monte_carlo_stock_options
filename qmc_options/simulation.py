"""
Geometric Brownian Motion simulation and Monte Carlo utilities.

This module provides functions for simulating stock price paths
and performing Monte Carlo integration.
"""

import numpy as np
from scipy import stats


def box_muller(mu: float = 0.0, sigma: float = 1.0, size: int = 1) -> np.ndarray:
    """
    Generate normal random variables using Box-Muller transform.

    Parameters
    ----------
    mu : float, default=0.0
        Mean of the normal distribution
    sigma : float, default=1.0
        Standard deviation
    size : int, default=1
        Number of samples to generate

    Returns
    -------
    np.ndarray
        Random samples from N(mu, sigma^2)
    """
    # For compatibility, but NumPy's built-in is faster
    # This is mainly for educational purposes
    U1 = np.random.rand(size)
    U2 = np.random.rand(size)

    Z = np.sqrt(-2 * np.log(U1)) * np.cos(2 * np.pi * U2)

    return sigma * Z + mu


def gbm_explicit(S0: float, r: float, sigma: float, delta: float,
                 n: int, T: float, Z: np.ndarray) -> float:
    """
    Compute n-th step of GBM using explicit formula.

    Uses the exact solution:
    S(n) = S0 * exp((r - delta - 0.5*sigma^2)*n*dt + sigma*sqrt(dt)*sum(Z[1:n]))

    Parameters
    ----------
    S0 : float
        Initial stock price
    r : float
        Risk-free interest rate
    sigma : float
        Volatility
    delta : float
        Dividend yield
    n : int
        Time step index (0 <= n <= len(Z))
    T : float
        Time to maturity
    Z : np.ndarray
        Vector of standard normal random variables

    Returns
    -------
    float
        Stock price at step n
    """
    m = len(Z)
    if n > m:
        raise ValueError(f"Step n={n} exceeds path length m={m}")

    if n == 0:
        return S0

    dt = T / m
    sum_Z = np.sum(Z[:n])

    aux1 = np.exp((r - delta - 0.5 * sigma ** 2) * n * dt)
    aux2 = np.exp(sigma * np.sqrt(dt) * sum_Z)

    return S0 * aux1 * aux2


def gbm_euler(S0: float, T: float, n: int, r: float,
              delta: float, sigma: float, seed: int = None) -> np.ndarray:
    """
    Generate GBM path using Euler-Maruyama discretization.

    Uses the approximation:
    S(i+1) = S(i) * (1 + (r - delta)*dt + sigma*sqrt(dt)*Z)

    Parameters
    ----------
    S0 : float
        Initial stock price
    T : float
        Time period
    n : int
        Number of time steps
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    np.ndarray
        Array of length n containing the simulated path
    """
    if seed is not None:
        np.random.seed(seed)

    dt = T / n
    path = np.zeros(n)
    path[0] = S0

    for i in range(1, n):
        Z = np.random.randn()
        path[i] = path[i-1] * (1 + (r - delta) * dt + sigma * np.sqrt(dt) * Z)

    return path


def gbm_exact(S0: float, T: float, n: int, r: float,
              delta: float, sigma: float, Z: np.ndarray = None) -> np.ndarray:
    """
    Generate GBM path using exact solution.

    S(t) = S0 * exp((r - delta - 0.5*sigma^2)*t + sigma*W(t))
    where W(t) is a Brownian motion.

    Parameters
    ----------
    S0 : float
        Initial stock price
    T : float
        Time period
    n : int
        Number of time steps
    r : float
        Risk-free interest rate
    delta : float
        Dividend yield
    sigma : float
        Volatility
    Z : np.ndarray, optional
        Pre-generated standard normal samples. If None, generated internally.

    Returns
    -------
    np.ndarray
        Array of length n+1 containing the simulated path (including S0)
    """
    dt = T / n

    if Z is None:
        Z = np.random.randn(n)
    elif len(Z) != n:
        raise ValueError(f"Z must have length {n}")

    # Cumulative Brownian motion
    dW = np.sqrt(dt) * Z
    W = np.concatenate([[0], np.cumsum(dW)])

    # Time grid
    t = np.linspace(0, T, n + 1)

    # Exact GBM solution
    path = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * t + sigma * W)

    return path


def generate_correlated_normals(N: int, rho: float, Z1: np.ndarray = None) -> tuple:
    """
    Generate two correlated standard normal random variables.

    Uses the Cholesky decomposition method:
    Z2 = rho * Z1 + sqrt(1 - rho^2) * Z_indep

    Parameters
    ----------
    N : int
        Number of samples
    rho : float
        Correlation coefficient (-1 <= rho <= 1)
    Z1 : np.ndarray, optional
        First set of standard normals. If None, generated internally.

    Returns
    -------
    tuple of np.ndarray
        (Z1, Z2) - two correlated normal random vectors
    """
    if Z1 is None:
        Z1 = np.random.randn(N)

    Z_indep = np.random.randn(N)
    Z2 = rho * Z1 + np.sqrt(1 - rho ** 2) * Z_indep

    return Z1, Z2


def qmc_to_normal(points: np.ndarray) -> np.ndarray:
    """
    Transform quasi-random points from [0,1]^d to standard normal.

    Uses inverse CDF (probit) transformation.

    Parameters
    ----------
    points : np.ndarray
        Quasi-random points in [0, 1)^d

    Returns
    -------
    np.ndarray
        Transformed points with standard normal distribution
    """
    # Avoid exactly 0 or 1 which give infinite values
    points_clipped = np.clip(points, 1e-10, 1 - 1e-10)
    return stats.norm.ppf(points_clipped)


def periodize(x: float) -> float:
    """
    Apply periodization transformation to map [0,1] to all of R.

    The transformation ensures smooth periodic extension which can
    improve QMC convergence rates.

    Parameters
    ----------
    x : float
        Value in [0, 1]

    Returns
    -------
    float
        Periodized value
    """
    if x < 0.5:
        return 2 * x
    else:
        return 2 * (1 - x)


def periodize_array(points: np.ndarray) -> np.ndarray:
    """
    Apply periodization transformation element-wise to an array.

    Parameters
    ----------
    points : np.ndarray
        Array of values in [0, 1]

    Returns
    -------
    np.ndarray
        Periodized array
    """
    result = np.where(points < 0.5, 2 * points, 2 * (1 - points))
    return result


def standard_error(samples: np.ndarray) -> float:
    """
    Compute standard error of Monte Carlo estimate.

    Parameters
    ----------
    samples : np.ndarray
        Array of Monte Carlo samples

    Returns
    -------
    float
        Standard error = std(samples) / sqrt(n)
    """
    n = len(samples)
    if n <= 1:
        return 0.0
    return np.std(samples, ddof=1) / np.sqrt(n)
