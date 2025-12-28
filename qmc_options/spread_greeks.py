"""
Greeks for spread options using importance sampling.

This module implements delta and gamma calculations for spread options
with two underlying assets using the importance sampling technique.
"""

import numpy as np
from scipy import stats


def _spread_integrand_base(u1: float, u2: float, w1: float, w2: float,
                           r: float, delta1: float, delta2: float,
                           S10: float, S20: float, sigma1: float, sigma2: float,
                           rho12: float, T: float, K: float):
    """
    Compute base quantities for spread option integrand.

    Returns dictionary with intermediate calculations used by
    price and Greeks computations.
    """
    # Safety check
    if u1 <= 0:
        return None

    # Drift-adjusted means
    mu1T = np.log(S10) + (r - delta1 - 0.5 * sigma1 ** 2) * T
    mu2T = np.log(S20) + (r - delta2 - 0.5 * sigma2 ** 2) * T

    # Cholesky decomposition
    c11 = sigma1 * np.sqrt(T)
    c21 = rho12 * sigma2 * np.sqrt(T)
    c22 = np.sqrt(1 - rho12 ** 2) * sigma2 * np.sqrt(T)

    # Transform uniform to normal
    inv_u1 = stats.norm.ppf(u1)

    # First underlying
    h3 = c11 * inv_u1 + mu1T
    h1 = w1 * np.exp(h3)

    # Conditional distribution parameter
    g = (np.log(h1 + K) - np.log(w2) - mu2T - c21 * inv_u1) / c22
    d2 = stats.norm.cdf(g)

    # Safety check for second transformation
    cond_u = d2 + u2 * (1 - d2)
    if cond_u >= 1:
        return None

    # Second underlying (conditional)
    h5 = stats.norm.ppf(cond_u)
    h4 = c21 * inv_u1 + c22 * h5 + mu2T
    h2 = w2 * np.exp(h4)

    # Payoff
    h = h2 - h1 - K

    return {
        'h1': h1, 'h2': h2, 'h': h,
        'h3': h3, 'h4': h4, 'h5': h5,
        'g': g, 'd2': d2,
        'inv_u1': inv_u1,
        'u2': u2,
        'c11': c11, 'c21': c21, 'c22': c22,
        'mu1T': mu1T, 'mu2T': mu2T
    }


def spread_delta1_integrand(u1: float, u2: float, w1: float, w2: float,
                            r: float, delta1: float, delta2: float,
                            S10: float, S20: float, sigma1: float, sigma2: float,
                            rho12: float, T: float, K: float) -> float:
    """
    Integrand for Delta with respect to first underlying (S1).

    Parameters
    ----------
    u1, u2 : float
        QMC points in [0, 1)
    w1, w2 : float
        Weights for each underlying
    r : float
        Risk-free rate
    delta1, delta2 : float
        Dividend yields
    S10, S20 : float
        Initial prices
    sigma1, sigma2 : float
        Volatilities
    rho12 : float
        Correlation
    T : float
        Time to maturity
    K : float
        Strike price

    Returns
    -------
    float
        Integrand value for delta1
    """
    base = _spread_integrand_base(u1, u2, w1, w2, r, delta1, delta2,
                                  S10, S20, sigma1, sigma2, rho12, T, K)
    if base is None:
        return 0.0

    h1, h2, h, h5, g, d2 = base['h1'], base['h2'], base['h'], base['h5'], base['g'], base['d2']
    u2, c22 = base['u2'], base['c22']

    # Partial derivatives with respect to S1
    term1 = (h2 / (h1 + K)) * (1 - u2) * np.exp(0.5 * (h5 ** 2 - g ** 2))
    partial_h_S1 = (h1 / S10) * (term1 - 1)

    partial_g_S1 = h1 / (c22 * (h1 + K) * S10)
    partial_d2_S1 = stats.norm.pdf(g) * partial_g_S1

    return (1 - d2) * partial_h_S1 - partial_d2_S1 * h


def spread_delta2_integrand(u1: float, u2: float, w1: float, w2: float,
                            r: float, delta1: float, delta2: float,
                            S10: float, S20: float, sigma1: float, sigma2: float,
                            rho12: float, T: float, K: float) -> float:
    """
    Integrand for Delta with respect to second underlying (S2).

    Similar to spread_delta1_integrand but for S2.
    """
    base = _spread_integrand_base(u1, u2, w1, w2, r, delta1, delta2,
                                  S10, S20, sigma1, sigma2, rho12, T, K)
    if base is None:
        return 0.0

    h1, h2, h, h5, g, d2 = base['h1'], base['h2'], base['h'], base['h5'], base['g'], base['d2']
    u2, c22 = base['u2'], base['c22']

    # Partial derivatives with respect to S2
    partial_h_S2 = (h2 / S20) * (1 - (1 - u2) * np.exp(0.5 * (h5 ** 2 - g ** 2)))
    partial_d2_S2 = -(h2 / S20) * stats.norm.pdf(g) / c22

    return (1 - d2) * partial_h_S2 - partial_d2_S2 * h


def spread_gamma1_integrand(u1: float, u2: float, w1: float, w2: float,
                            r: float, delta1: float, delta2: float,
                            S10: float, S20: float, sigma1: float, sigma2: float,
                            rho12: float, T: float, K: float) -> float:
    """
    Integrand for Gamma with respect to first underlying (S1).

    Computes second partial derivative ∂²V/∂S1².
    """
    base = _spread_integrand_base(u1, u2, w1, w2, r, delta1, delta2,
                                  S10, S20, sigma1, sigma2, rho12, T, K)
    if base is None:
        return 0.0

    h1, h2, h, h5, g, d2 = base['h1'], base['h2'], base['h'], base['h5'], base['g'], base['d2']
    u2, c22 = base['u2'], base['c22']

    # Intermediate calculations
    a1 = h1 / ((h1 + K) * S10)
    a2 = h5 ** 2 - g ** 2

    # First derivatives
    dp_h_S1 = (h1 / S10) * ((h2 / (h1 + K)) * (1 - u2) * np.exp(0.5 * a2) - 1)
    dp_g_S1 = a1 / c22
    dp_d2_S1 = stats.norm.pdf(g) * dp_g_S1

    # Second derivatives
    term1 = (1 - u2) * np.exp(0.5 * a2) * (h5 / c22 + 1)
    term2 = g / c22 + 1
    dp_2_h_S1 = h2 * a1 * a1 * (1 - u2) * np.exp(0.5 * a2) * (term1 - term2)

    dp_2_g_S1 = -a1 * a1 / c22
    dp_2_d2_S1 = dp_d2_S1 * ((dp_2_g_S1 / dp_g_S1) - dp_g_S1 * g)

    return (1 - d2) * dp_2_h_S1 - 2 * dp_h_S1 * dp_d2_S1 - dp_2_d2_S1 * h


def spread_gamma2_integrand(u1: float, u2: float, w1: float, w2: float,
                            r: float, delta1: float, delta2: float,
                            S10: float, S20: float, sigma1: float, sigma2: float,
                            rho12: float, T: float, K: float) -> float:
    """
    Integrand for Gamma with respect to second underlying (S2).

    Computes second partial derivative ∂²V/∂S2².
    """
    base = _spread_integrand_base(u1, u2, w1, w2, r, delta1, delta2,
                                  S10, S20, sigma1, sigma2, rho12, T, K)
    if base is None:
        return 0.0

    h1, h2, h, h5, g, d2 = base['h1'], base['h2'], base['h'], base['h5'], base['g'], base['d2']
    u2, c22 = base['u2'], base['c22']

    # Intermediate calculations
    a1 = h2 / (S20 * c22)
    a2 = h5 ** 2 - g ** 2

    # First derivatives
    dp_h_S2 = (h2 / S20) * (1 - (1 - u2) * np.exp(0.5 * a2))
    dp_d2_S2 = -a1 * stats.norm.pdf(g)

    # Second derivatives
    term1 = (1 - u2) * np.exp(0.5 * a2)
    dp_2_h_S2 = a1 * a1 * term1 * (term1 * (h5 / c22 - 1) - g / c22)

    dp_2_d2_S2 = a1 * a1 * stats.norm.pdf(g) * (g / c22 - 1)

    return (1 - d2) * dp_2_h_S2 - 2 * dp_h_S2 * dp_d2_S2 - dp_2_d2_S2 * h


def spread_delta1(points: np.ndarray, w1: float, w2: float, r: float, K: float,
                  S10: float, S20: float, delta1: float, delta2: float,
                  sigma1: float, sigma2: float, rho12: float, T: float,
                  periodization: int = 8) -> float:
    """
    Compute Delta for spread option with respect to S1.

    Parameters
    ----------
    points : np.ndarray
        QMC points of shape (N, 2)
    w1, w2 : float
        Weights
    r : float
        Risk-free rate
    K : float
        Strike
    S10, S20 : float
        Initial prices
    delta1, delta2 : float
        Dividend yields
    sigma1, sigma2 : float
        Volatilities
    rho12 : float
        Correlation
    T : float
        Time to maturity
    periodization : int
        Periodization parameter (1-8, default 8 = identity)

    Returns
    -------
    float
        Delta1
    """
    from .periodization import PeriodicTransform

    N = len(points)
    value = 0.0

    for i in range(N):
        # Apply periodization
        u1 = PeriodicTransform.transform(np.array([points[i, 0]]), periodization)[0]
        u2 = PeriodicTransform.transform(np.array([points[i, 1]]), periodization)[0]

        # Jacobian from periodization
        du1 = PeriodicTransform.derivative(np.array([points[i, 0]]), periodization)[0]
        du2 = PeriodicTransform.derivative(np.array([points[i, 1]]), periodization)[0]
        jacobian = du1 * du2

        # Integrand value
        integrand = spread_delta1_integrand(u1, u2, w1, w2, r, delta1, delta2,
                                           S10, S20, sigma1, sigma2, rho12, T, K)

        value += integrand * jacobian

    return np.exp(-r * T) * value / N


def spread_delta2(points: np.ndarray, w1: float, w2: float, r: float, K: float,
                  S10: float, S20: float, delta1: float, delta2: float,
                  sigma1: float, sigma2: float, rho12: float, T: float,
                  periodization: int = 8) -> float:
    """Compute Delta for spread option with respect to S2."""
    from .periodization import PeriodicTransform

    N = len(points)
    value = 0.0

    for i in range(N):
        u1 = PeriodicTransform.transform(np.array([points[i, 0]]), periodization)[0]
        u2 = PeriodicTransform.transform(np.array([points[i, 1]]), periodization)[0]

        du1 = PeriodicTransform.derivative(np.array([points[i, 0]]), periodization)[0]
        du2 = PeriodicTransform.derivative(np.array([points[i, 1]]), periodization)[0]
        jacobian = du1 * du2

        integrand = spread_delta2_integrand(u1, u2, w1, w2, r, delta1, delta2,
                                           S10, S20, sigma1, sigma2, rho12, T, K)

        value += integrand * jacobian

    return np.exp(-r * T) * value / N


def spread_gamma1(points: np.ndarray, w1: float, w2: float, r: float, K: float,
                  S10: float, S20: float, delta1: float, delta2: float,
                  sigma1: float, sigma2: float, rho12: float, T: float,
                  periodization: int = 8) -> float:
    """Compute Gamma for spread option with respect to S1."""
    from .periodization import PeriodicTransform

    N = len(points)
    value = 0.0

    for i in range(N):
        u1 = PeriodicTransform.transform(np.array([points[i, 0]]), periodization)[0]
        u2 = PeriodicTransform.transform(np.array([points[i, 1]]), periodization)[0]

        du1 = PeriodicTransform.derivative(np.array([points[i, 0]]), periodization)[0]
        du2 = PeriodicTransform.derivative(np.array([points[i, 1]]), periodization)[0]
        jacobian = du1 * du2

        integrand = spread_gamma1_integrand(u1, u2, w1, w2, r, delta1, delta2,
                                           S10, S20, sigma1, sigma2, rho12, T, K)

        value += integrand * jacobian

    return np.exp(-r * T) * value / N


def spread_gamma2(points: np.ndarray, w1: float, w2: float, r: float, K: float,
                  S10: float, S20: float, delta1: float, delta2: float,
                  sigma1: float, sigma2: float, rho12: float, T: float,
                  periodization: int = 8) -> float:
    """Compute Gamma for spread option with respect to S2."""
    from .periodization import PeriodicTransform

    N = len(points)
    value = 0.0

    for i in range(N):
        u1 = PeriodicTransform.transform(np.array([points[i, 0]]), periodization)[0]
        u2 = PeriodicTransform.transform(np.array([points[i, 1]]), periodization)[0]

        du1 = PeriodicTransform.derivative(np.array([points[i, 0]]), periodization)[0]
        du2 = PeriodicTransform.derivative(np.array([points[i, 1]]), periodization)[0]
        jacobian = du1 * du2

        integrand = spread_gamma2_integrand(u1, u2, w1, w2, r, delta1, delta2,
                                           S10, S20, sigma1, sigma2, rho12, T, K)

        value += integrand * jacobian

    return np.exp(-r * T) * value / N
