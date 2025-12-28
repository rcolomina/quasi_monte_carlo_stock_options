"""
Greeks estimation using pathwise and likelihood ratio methods.

This module implements Monte Carlo estimators for option sensitivities:
- Pathwise derivative method
- Likelihood ratio (score function) method
"""

import numpy as np
from scipy import stats


def pathwise_delta_european_call(S0: float, K: float, r: float, delta: float,
                                  sigma: float, T: float, points: np.ndarray) -> float:
    """
    Estimate Delta using pathwise derivative method for European call.

    Delta = ∂V/∂S₀

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
        QMC points in [0,1)

    Returns
    -------
    float
        Delta estimate
    """
    N = len(points)
    delta_sum = 0.0

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            ST = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)

            if ST > K:  # Option is in the money
                delta_sum += ST / S0

    return np.exp(-r * T) * delta_sum / N


def pathwise_gamma_european_call(S0: float, K: float, r: float, delta: float,
                                  sigma: float, T: float, points: np.ndarray) -> float:
    """
    Estimate Gamma using pathwise derivative method for European call.

    Gamma = ∂²V/∂S₀²

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
        QMC points in [0,1)

    Returns
    -------
    float
        Gamma estimate
    """
    N = len(points)
    gamma_sum = 0.0

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            x = (r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z
            ST = S0 * np.exp(x)

            if ST > K:  # Option is in the money
                gamma_sum += (ST / (S0 ** 2)) * (x / S0)

    return np.exp(-r * T) * gamma_sum / N


def pathwise_vega_european_call(S0: float, K: float, r: float, delta: float,
                                 sigma: float, T: float, points: np.ndarray) -> float:
    """
    Estimate Vega using pathwise derivative method for European call.

    Vega = ∂V/∂σ

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
        QMC points in [0,1)

    Returns
    -------
    float
        Vega estimate
    """
    N = len(points)
    vega_sum = 0.0

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            ST = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)

            if ST > K:  # Option is in the money
                vega_sum += ST * (-sigma * T + np.sqrt(T) * Z)

    return np.exp(-r * T) * vega_sum / N


def pathwise_rho_european_call(S0: float, K: float, r: float, delta: float,
                                sigma: float, T: float, points: np.ndarray) -> float:
    """
    Estimate Rho using pathwise derivative method for European call.

    Rho = ∂V/∂r

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
        QMC points in [0,1)

    Returns
    -------
    float
        Rho estimate
    """
    N = len(points)
    rho_sum = 0.0
    payoff_sum = 0.0

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            ST = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
            payoff = max(ST - K, 0)

            if ST > K:
                rho_sum += ST * T

            payoff_sum += payoff

    # Rho includes discounting derivative
    price = np.exp(-r * T) * payoff_sum / N
    pathwise_term = np.exp(-r * T) * rho_sum / N

    return pathwise_term - T * price


# Likelihood ratio (score function) methods

def likelihood_delta_european_call(S0: float, K: float, r: float, delta: float,
                                    sigma: float, T: float, points: np.ndarray) -> float:
    """
    Estimate Delta using likelihood ratio method for European call.

    Uses score function: ∂ln(f)/∂S₀ where f is the density.

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
        QMC points in [0,1)

    Returns
    -------
    float
        Delta estimate
    """
    N = len(points)
    delta_sum = 0.0

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            ST = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
            payoff = max(ST - K, 0)

            # Score function for S0
            score = Z / (S0 * sigma * np.sqrt(T))
            delta_sum += payoff * score

    return np.exp(-r * T) * delta_sum / N


def likelihood_gamma_european_call(S0: float, K: float, r: float, delta: float,
                                    sigma: float, T: float, points: np.ndarray) -> float:
    """
    Estimate Gamma using likelihood ratio method for European call.

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
        QMC points in [0,1)

    Returns
    -------
    float
        Gamma estimate
    """
    N = len(points)
    gamma_sum = 0.0

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            ST = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
            payoff = max(ST - K, 0)

            # Second derivative of log-likelihood
            term = (Z ** 2 - 1) / (sigma ** 2 * T) - Z / (S0 * sigma * np.sqrt(T))
            term /= S0

            gamma_sum += payoff * term

    return np.exp(-r * T) * gamma_sum / N


def likelihood_vega_european_call(S0: float, K: float, r: float, delta: float,
                                   sigma: float, T: float, points: np.ndarray) -> float:
    """
    Estimate Vega using likelihood ratio method for European call.

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
        QMC points in [0,1)

    Returns
    -------
    float
        Vega estimate
    """
    N = len(points)
    vega_sum = 0.0

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            ST = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
            payoff = max(ST - K, 0)

            # Score function for sigma
            score = (Z ** 2 - 1) / sigma - Z * np.sqrt(T)

            vega_sum += payoff * score

    return np.exp(-r * T) * vega_sum / N


def likelihood_theta_european_call(S0: float, K: float, r: float, delta: float,
                                    sigma: float, T: float, points: np.ndarray) -> float:
    """
    Estimate Theta using likelihood ratio method for European call.

    Theta = -∂V/∂T

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
        QMC points in [0,1)

    Returns
    -------
    float
        Theta estimate
    """
    N = len(points)
    theta_sum = 0.0
    payoff_sum = 0.0

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            ST = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
            payoff = max(ST - K, 0)

            # Score function for T
            score = (r - delta - 0.5 * sigma ** 2) + sigma * Z / (2 * np.sqrt(T))

            theta_sum += payoff * score
            payoff_sum += payoff

    price = np.exp(-r * T) * payoff_sum / N
    score_term = np.exp(-r * T) * theta_sum / N

    # Theta includes discounting derivative (negative sign convention)
    return -(score_term + r * price)


def likelihood_rho_european_call(S0: float, K: float, r: float, delta: float,
                                  sigma: float, T: float, points: np.ndarray) -> float:
    """
    Estimate Rho using likelihood ratio method for European call.

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
        QMC points in [0,1)

    Returns
    -------
    float
        Rho estimate
    """
    N = len(points)
    rho_sum = 0.0
    payoff_sum = 0.0

    for i in range(N):
        if points[i] > 0:
            Z = stats.norm.ppf(points[i])
            ST = S0 * np.exp((r - delta - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
            payoff = max(ST - K, 0)

            # Score function for r (from drift term)
            rho_sum += payoff * T
            payoff_sum += payoff

    price = np.exp(-r * T) * payoff_sum / N
    score_term = np.exp(-r * T) * rho_sum / N

    # Rho includes discounting derivative
    return score_term - T * price
