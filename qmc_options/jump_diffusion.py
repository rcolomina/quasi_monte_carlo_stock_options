"""
Jump-diffusion models for more realistic option pricing.

Implements:
- Merton jump-diffusion
- Kou double exponential jumps
- Variance Gamma process
"""

import numpy as np
from scipy import stats


def merton_jump_diffusion(S0: float, r: float, sigma: float, delta: float,
                          T: float, n_steps: int,
                          lambda_jump: float, mu_jump: float, sigma_jump: float,
                          Z: np.ndarray = None, seed: int = None) -> np.ndarray:
    """
    Simulate stock price path using Merton jump-diffusion model.

    dS/S = (r - delta - λk)dt + σdW + dJ

    where J are log-normal jumps with mean μ_J and volatility σ_J

    Parameters
    ----------
    S0 : float
        Initial stock price
    r : float
        Risk-free rate
    sigma : float
        Diffusion volatility (continuous component)
    delta : float
        Dividend yield
    T : float
        Time horizon
    n_steps : int
        Number of time steps
    lambda_jump : float
        Jump intensity (average number of jumps per year)
    mu_jump : float
        Mean of log-jump size
    sigma_jump : float
        Volatility of log-jump size
    Z : np.ndarray, optional
        Pre-generated normal random variables (for QMC)
    seed : int, optional
        Random seed

    Returns
    -------
    np.ndarray
        Simulated price path of length n_steps + 1
    """
    if seed is not None:
        np.random.seed(seed)

    dt = T / n_steps

    # Expected jump size adjustment
    k = np.exp(mu_jump + 0.5 * sigma_jump**2) - 1

    # Drift adjustment for jumps (martingale correction)
    drift = r - delta - lambda_jump * k - 0.5 * sigma**2

    # Generate Brownian increments
    if Z is None:
        Z = np.random.randn(n_steps)

    # Generate jump times (Poisson process)
    n_jumps = np.random.poisson(lambda_jump * T)
    jump_times = np.sort(np.random.uniform(0, T, n_jumps))

    # Generate jump sizes (log-normal)
    if n_jumps > 0:
        jump_sizes = np.exp(np.random.normal(mu_jump, sigma_jump, n_jumps))
    else:
        jump_sizes = np.array([])

    # Simulate path
    path = np.zeros(n_steps + 1)
    path[0] = S0

    jump_idx = 0
    for i in range(n_steps):
        t = i * dt

        # Continuous diffusion component
        dW = sigma * np.sqrt(dt) * Z[i]
        path[i + 1] = path[i] * np.exp(drift * dt + dW)

        # Add jumps that occur in this time step
        while jump_idx < n_jumps and jump_times[jump_idx] <= t + dt:
            path[i + 1] *= jump_sizes[jump_idx]
            jump_idx += 1

    return path


def kou_double_exponential(S0: float, r: float, sigma: float, delta: float,
                           T: float, n_steps: int,
                           lambda_jump: float, p_up: float,
                           eta_up: float, eta_down: float,
                           Z: np.ndarray = None, seed: int = None) -> np.ndarray:
    """
    Simulate stock price using Kou double exponential jump-diffusion.

    Jump sizes follow asymmetric double exponential distribution:
    - Upward jumps: exponential with rate η₁
    - Downward jumps: exponential with rate η₂

    Better captures:
    - Fat tails in returns
    - Asymmetric jumps (crashes vs rallies)

    Parameters
    ----------
    S0 : float
        Initial stock price
    r : float
        Risk-free rate
    sigma : float
        Diffusion volatility
    delta : float
        Dividend yield
    T : float
        Time horizon
    n_steps : int
        Number of time steps
    lambda_jump : float
        Jump intensity
    p_up : float
        Probability of upward jump (0 < p < 1)
    eta_up : float
        Exponential rate for upward jumps (η₁ > 1)
    eta_down : float
        Exponential rate for downward jumps (η₂ > 0)
    Z : np.ndarray, optional
        Pre-generated normal random variables
    seed : int, optional
        Random seed

    Returns
    -------
    np.ndarray
        Simulated price path
    """
    if seed is not None:
        np.random.seed(seed)

    dt = T / n_steps

    # Expected jump size
    k = p_up * eta_up / (eta_up - 1) + (1 - p_up) * eta_down / (eta_down + 1) - 1

    # Drift adjustment
    drift = r - delta - lambda_jump * k - 0.5 * sigma**2

    # Generate Brownian increments
    if Z is None:
        Z = np.random.randn(n_steps)

    # Generate jumps
    n_jumps = np.random.poisson(lambda_jump * T)
    jump_times = np.sort(np.random.uniform(0, T, n_jumps))

    # Generate jump sizes (double exponential)
    jump_sizes = np.zeros(n_jumps)
    for j in range(n_jumps):
        if np.random.rand() < p_up:
            # Upward jump
            Y = np.random.exponential(1 / eta_up)
        else:
            # Downward jump
            Y = -np.random.exponential(1 / eta_down)
        jump_sizes[j] = np.exp(Y)

    # Simulate path
    path = np.zeros(n_steps + 1)
    path[0] = S0

    jump_idx = 0
    for i in range(n_steps):
        t = i * dt

        # Diffusion
        dW = sigma * np.sqrt(dt) * Z[i]
        path[i + 1] = path[i] * np.exp(drift * dt + dW)

        # Jumps
        while jump_idx < n_jumps and jump_times[jump_idx] <= t + dt:
            path[i + 1] *= jump_sizes[jump_idx]
            jump_idx += 1

    return path


def variance_gamma_process(S0: float, r: float, delta: float, T: float, n_steps: int,
                           sigma: float, nu: float, theta: float,
                           seed: int = None) -> np.ndarray:
    """
    Simulate stock price using Variance Gamma process.

    Infinite activity pure jump process (no diffusion component).
    Can model:
    - Heavy tails
    - Skewness
    - Kurtosis

    Parameters
    ----------
    S0 : float
        Initial stock price
    r : float
        Risk-free rate
    delta : float
        Dividend yield
    T : float
        Time horizon
    n_steps : int
        Number of time steps
    sigma : float
        Volatility parameter
    nu : float
        Variance rate of Gamma time change (controls kurtosis)
    theta : float
        Drift of Brownian motion (controls skewness)
    seed : int, optional
        Random seed

    Returns
    -------
    np.ndarray
        Simulated price path
    """
    if seed is not None:
        np.random.seed(seed)

    dt = T / n_steps

    # Gamma time change
    gamma_increments = np.random.gamma(dt / nu, nu, n_steps)

    # Brownian motion with drift
    normal_increments = np.random.randn(n_steps)
    X_increments = theta * gamma_increments + sigma * np.sqrt(gamma_increments) * normal_increments

    # Martingale correction
    omega = (1 / nu) * np.log(1 - theta * nu - 0.5 * sigma**2 * nu)

    # Log-price process
    log_price = np.zeros(n_steps + 1)
    log_price[0] = np.log(S0)

    for i in range(n_steps):
        log_price[i + 1] = log_price[i] + (r - delta + omega) * dt + X_increments[i]

    return np.exp(log_price)


def european_call_merton_mc(S0: float, K: float, r: float, delta: float,
                            sigma: float, T: float,
                            lambda_jump: float, mu_jump: float, sigma_jump: float,
                            points: np.ndarray) -> tuple:
    """
    Price European call under Merton jump-diffusion using QMC.

    Parameters
    ----------
    S0 : float
        Initial stock price
    K : float
        Strike price
    r : float
        Risk-free rate
    delta : float
        Dividend yield
    sigma : float
        Diffusion volatility
    T : float
        Time to maturity
    lambda_jump : float
        Jump intensity
    mu_jump : float
        Mean log-jump size
    sigma_jump : float
        Jump volatility
    points : np.ndarray
        QMC points in [0, 1)

    Returns
    -------
    tuple
        (price, standard_error)
    """
    from .simulation import qmc_to_normal

    N = len(points)
    payoffs = np.zeros(N)

    # Expected jump adjustment
    k = np.exp(mu_jump + 0.5 * sigma_jump**2) - 1

    for i in range(N):
        if points[i] > 0:
            # Transform to normal
            Z = stats.norm.ppf(points[i])

            # Simulate number of jumps (Poisson)
            n_jumps = np.random.poisson(lambda_jump * T)

            # Simulate terminal price
            # Diffusion component
            drift = r - delta - lambda_jump * k - 0.5 * sigma**2
            ST_diffusion = S0 * np.exp(drift * T + sigma * np.sqrt(T) * Z)

            # Jump component
            if n_jumps > 0:
                jump_total = np.sum(np.random.normal(mu_jump, sigma_jump, n_jumps))
                ST = ST_diffusion * np.exp(jump_total)
            else:
                ST = ST_diffusion

            payoffs[i] = max(ST - K, 0)

    price = np.exp(-r * T) * np.mean(payoffs)
    std_error = np.std(payoffs, ddof=1) / np.sqrt(N)

    return price, std_error


def calibrate_merton_to_market(S0: float, r: float, delta: float, T: float,
                                market_options: list) -> dict:
    """
    Calibrate Merton jump-diffusion parameters to market option prices.

    Uses least-squares optimization to find (σ, λ, μ_J, σ_J) that minimize
    pricing errors vs market.

    Parameters
    ----------
    S0 : float
        Current stock price
    r : float
        Risk-free rate
    delta : float
        Dividend yield
    T : float
        Time to maturity
    market_options : list of dict
        Each dict has {'K': strike, 'price': market_price, 'type': 'call'/'put'}

    Returns
    -------
    dict
        Calibrated parameters: {'sigma', 'lambda_jump', 'mu_jump', 'sigma_jump'}
    """
    from scipy.optimize import minimize
    from qmc_options import generators

    # Generate QMC points once
    qmc_points = generators.halton([2], 5000)[:, 0]

    def objective(params):
        sigma, lambda_jump, mu_jump, sigma_jump = params

        # Ensure parameters are valid
        if sigma <= 0 or lambda_jump < 0 or sigma_jump < 0:
            return 1e10

        total_error = 0
        for opt in market_options:
            K = opt['K']
            market_price = opt['price']

            model_price, _ = european_call_merton_mc(
                S0, K, r, delta, sigma, T,
                lambda_jump, mu_jump, sigma_jump,
                qmc_points
            )

            # Relative error
            error = ((model_price - market_price) / market_price) ** 2
            total_error += error

        return total_error

    # Initial guess
    x0 = [0.25, 1.0, -0.1, 0.3]  # [sigma, lambda, mu_J, sigma_J]

    # Bounds
    bounds = [(0.01, 1.0), (0, 10), (-1, 1), (0.01, 1)]

    result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)

    return {
        'sigma': result.x[0],
        'lambda_jump': result.x[1],
        'mu_jump': result.x[2],
        'sigma_jump': result.x[3],
        'calibration_error': result.fun
    }
