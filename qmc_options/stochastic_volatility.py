"""
Stochastic volatility models (Heston, SABR).

These models allow volatility to evolve randomly, capturing:
- Volatility clustering
- Volatility smile/skew
- More realistic dynamics
"""

import numpy as np
from scipy import stats


def heston_model(S0: float, V0: float, r: float, delta: float, T: float, n_steps: int,
                kappa: float, theta: float, sigma_v: float, rho: float,
                Z: np.ndarray = None, seed: int = None) -> tuple:
    """
    Simulate stock price and variance using Heston stochastic volatility model.

    dS/S = (r - delta)dt + √V dW₁
    dV = κ(θ - V)dt + σᵥ√V dW₂

    where Corr(dW₁, dW₂) = ρ

    Parameters
    ----------
    S0 : float
        Initial stock price
    V0 : float
        Initial variance (σ₀²)
    r : float
        Risk-free rate
    delta : float
        Dividend yield
    T : float
        Time horizon
    n_steps : int
        Number of time steps
    kappa : float
        Mean reversion speed (how fast V reverts to θ)
    theta : float
        Long-run variance (average σ²)
    sigma_v : float
        Volatility of volatility (vol-of-vol)
    rho : float
        Correlation between stock and variance (-1 ≤ ρ ≤ 1)
        Negative ρ: leverage effect (vol ↑ when price ↓)
    Z : np.ndarray, optional
        Pre-generated normal random variables (N×2) for QMC
    seed : int, optional
        Random seed

    Returns
    -------
    tuple
        (S_path, V_path) - stock price and variance paths
    """
    if seed is not None:
        np.random.seed(seed)

    dt = T / n_steps

    # Generate correlated Brownian motions
    if Z is None:
        Z = np.random.randn(n_steps, 2)

    # Apply correlation structure
    Z1 = Z[:, 0]
    Z2 = rho * Z[:, 0] + np.sqrt(1 - rho**2) * Z[:, 1]

    # Initialize paths
    S = np.zeros(n_steps + 1)
    V = np.zeros(n_steps + 1)
    S[0] = S0
    V[0] = V0

    # Euler discretization (full truncation scheme)
    for i in range(n_steps):
        # Variance process (ensure V stays positive)
        V[i + 1] = V[i] + kappa * (theta - V[i]) * dt + sigma_v * np.sqrt(max(V[i], 0)) * np.sqrt(dt) * Z2[i]
        V[i + 1] = max(V[i + 1], 0)  # Truncation to ensure positivity

        # Stock price process
        S[i + 1] = S[i] * np.exp((r - delta - 0.5 * V[i]) * dt + np.sqrt(max(V[i], 0)) * np.sqrt(dt) * Z1[i])

    return S, V


def heston_qe_scheme(S0: float, V0: float, r: float, delta: float, T: float, n_steps: int,
                    kappa: float, theta: float, sigma_v: float, rho: float,
                    Z: np.ndarray = None, seed: int = None) -> tuple:
    """
    Simulate Heston model using Quadratic-Exponential (QE) scheme.

    More accurate than Euler, especially for small V and large σᵥ.
    Better preserves the Feller condition: 2κθ > σᵥ²

    This is the **recommended production method** for Heston simulation.

    Returns
    -------
    tuple
        (S_path, V_path)
    """
    if seed is not None:
        np.random.seed(seed)

    dt = T / n_steps

    if Z is None:
        Z = np.random.randn(n_steps, 2)

    Z1 = Z[:, 0]
    Z2 = rho * Z[:, 0] + np.sqrt(1 - rho**2) * Z[:, 1]

    S = np.zeros(n_steps + 1)
    V = np.zeros(n_steps + 1)
    S[0] = S0
    V[0] = V0

    # Critical value (Andersen 2008)
    psi_c = 1.5

    for i in range(n_steps):
        # Variance simulation (QE scheme)
        m = theta + (V[i] - theta) * np.exp(-kappa * dt)
        s2 = (V[i] * sigma_v**2 * np.exp(-kappa * dt) / kappa * (1 - np.exp(-kappa * dt)) +
              theta * sigma_v**2 / (2 * kappa) * (1 - np.exp(-kappa * dt))**2)

        psi = s2 / m**2

        if psi <= psi_c:
            # Quadratic scheme
            b2 = 2 / psi - 1 + np.sqrt(2 / psi) * np.sqrt(2 / psi - 1)
            a = m / (1 + b2)
            U = np.random.rand()
            V[i + 1] = a * (np.sqrt(b2) + stats.norm.ppf(U))**2
        else:
            # Exponential scheme
            p = (psi - 1) / (psi + 1)
            beta = (1 - p) / m
            U = np.random.rand()
            if U <= p:
                V[i + 1] = 0
            else:
                V[i + 1] = np.log((1 - p) / (1 - U)) / beta

        # Stock price (exact discretization conditional on V path)
        K0 = (r - delta) * dt - rho / sigma_v * (V[i + 1] - V[i] - kappa * theta * dt)
        K0 += rho * kappa / sigma_v * V[i] * dt

        K1 = (rho * kappa / sigma_v - 0.5) * dt
        K2 = rho / sigma_v * dt
        K3 = (1 - rho**2) * dt

        S[i + 1] = S[i] * np.exp(K0 + K1 * V[i] + K2 * V[i + 1] + np.sqrt(K3 * V[i + 1]) * Z1[i])

    return S, V


def european_call_heston_mc(S0: float, V0: float, K: float, r: float, delta: float, T: float,
                            kappa: float, theta: float, sigma_v: float, rho: float,
                            N: int = 10000, use_qe: bool = True) -> tuple:
    """
    Price European call option under Heston model using Monte Carlo.

    Parameters
    ----------
    S0 : float
        Initial stock price
    V0 : float
        Initial variance
    K : float
        Strike price
    r : float
        Risk-free rate
    delta : float
        Dividend yield
    T : float
        Time to maturity
    kappa : float
        Mean reversion speed
    theta : float
        Long-run variance
    sigma_v : float
        Vol-of-vol
    rho : float
        Correlation
    N : int
        Number of MC simulations
    use_qe : bool
        Use QE scheme (True) or Euler (False)

    Returns
    -------
    tuple
        (price, standard_error)
    """
    n_steps = 252  # Daily steps

    payoffs = np.zeros(N)

    for i in range(N):
        if use_qe:
            S_path, _ = heston_qe_scheme(S0, V0, r, delta, T, n_steps,
                                        kappa, theta, sigma_v, rho)
        else:
            S_path, _ = heston_model(S0, V0, r, delta, T, n_steps,
                                    kappa, theta, sigma_v, rho)

        payoffs[i] = max(S_path[-1] - K, 0)

    price = np.exp(-r * T) * np.mean(payoffs)
    std_error = np.std(payoffs, ddof=1) / np.sqrt(N)

    return price, std_error


def implied_volatility_surface(S0: float, r: float, delta: float,
                               strikes: np.ndarray, maturities: np.ndarray,
                               heston_params: dict) -> np.ndarray:
    """
    Generate implied volatility surface from Heston parameters.

    Useful for:
    - Visualizing model fit
    - Comparing to market IV surface
    - Sanity checking calibration

    Parameters
    ----------
    S0 : float
        Current stock price
    r : float
        Risk-free rate
    delta : float
        Dividend yield
    strikes : np.ndarray
        Array of strike prices
    maturities : np.ndarray
        Array of maturities (years)
    heston_params : dict
        {'V0', 'kappa', 'theta', 'sigma_v', 'rho'}

    Returns
    -------
    np.ndarray
        Implied volatility surface (len(strikes) × len(maturities))
    """
    from qmc_options import analytical

    iv_surface = np.zeros((len(strikes), len(maturities)))

    for i, K in enumerate(strikes):
        for j, T in enumerate(maturities):
            # Price option under Heston
            heston_price, _ = european_call_heston_mc(
                S0, heston_params['V0'], K, r, delta, T,
                heston_params['kappa'], heston_params['theta'],
                heston_params['sigma_v'], heston_params['rho'],
                N=5000
            )

            # Implied volatility via Black-Scholes inversion
            # (Numerical root finding)
            from scipy.optimize import brentq

            def objective(sigma):
                bs_price = analytical.black_scholes_call(S0, K, r, delta, sigma, T)
                return bs_price - heston_price

            try:
                iv = brentq(objective, 0.01, 2.0)
                iv_surface[i, j] = iv
            except:
                iv_surface[i, j] = np.nan

    return iv_surface


def calibrate_heston_to_surface(S0: float, r: float, delta: float,
                                market_data: list) -> dict:
    """
    Calibrate Heston parameters to market implied volatility surface.

    Parameters
    ----------
    S0 : float
        Current stock price
    r : float
        Risk-free rate
    delta : float
        Dividend yield
    market_data : list of dict
        Each: {'K': strike, 'T': maturity, 'price': market_price}

    Returns
    -------
    dict
        Calibrated Heston parameters
    """
    from scipy.optimize import minimize

    def objective(params):
        V0, kappa, theta, sigma_v, rho = params

        # Feller condition check
        if 2 * kappa * theta < sigma_v**2:
            return 1e10

        # Parameter bounds check
        if V0 <= 0 or kappa <= 0 or theta <= 0 or sigma_v <= 0:
            return 1e10
        if abs(rho) >= 1:
            return 1e10

        total_error = 0
        for data in market_data:
            K, T, market_price = data['K'], data['T'], data['price']

            model_price, _ = european_call_heston_mc(
                S0, V0, K, r, delta, T,
                kappa, theta, sigma_v, rho,
                N=2000, use_qe=True
            )

            error = ((model_price - market_price) / market_price) ** 2
            total_error += error

        return total_error

    # Initial guess
    x0 = [0.04, 2.0, 0.04, 0.3, -0.5]  # [V0, kappa, theta, sigma_v, rho]

    # Bounds
    bounds = [(0.001, 1), (0.01, 10), (0.001, 1), (0.01, 2), (-0.99, 0.99)]

    result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds,
                     options={'maxiter': 100})

    return {
        'V0': result.x[0],
        'kappa': result.x[1],
        'theta': result.x[2],
        'sigma_v': result.x[3],
        'rho': result.x[4],
        'calibration_error': result.fun
    }
