"""
Utility functions for option pricing and analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compute_relative_error(mc_price: float, analytical_price: float) -> float:
    """
    Compute relative error between MC and analytical price.

    Parameters
    ----------
    mc_price : float
        Monte Carlo estimated price
    analytical_price : float
        Analytical (true) price

    Returns
    -------
    float
        Relative error as percentage
    """
    if analytical_price == 0:
        return 0.0
    return abs((mc_price - analytical_price) / analytical_price) * 100


def convergence_analysis(prices: np.ndarray, sample_sizes: np.ndarray,
                         analytical_price: float = None) -> pd.DataFrame:
    """
    Analyze convergence of MC/QMC pricing.

    Parameters
    ----------
    prices : np.ndarray
        Array of estimated prices for different sample sizes
    sample_sizes : np.ndarray
        Array of sample sizes used
    analytical_price : float, optional
        True price for error calculation

    Returns
    -------
    pd.DataFrame
        Convergence analysis results
    """
    results = pd.DataFrame({
        'N': sample_sizes,
        'Price': prices
    })

    if analytical_price is not None:
        results['Abs Error'] = np.abs(prices - analytical_price)
        results['Rel Error (%)'] = (results['Abs Error'] / analytical_price) * 100

    return results


def plot_convergence(sample_sizes: np.ndarray, errors: np.ndarray,
                     method_name: str = 'MC', log_scale: bool = True,
                     reference_rate: float = 0.5, save_path: str = None):
    """
    Plot convergence of MC/QMC method.

    Parameters
    ----------
    sample_sizes : np.ndarray
        Array of sample sizes
    errors : np.ndarray
        Array of errors for each sample size
    method_name : str
        Name of the method (for labeling)
    log_scale : bool
        Use log-log scale
    reference_rate : float
        Reference convergence rate (0.5 for MC, 1.0 for QMC)
    save_path : str, optional
        Path to save the plot
    """
    plt.figure(figsize=(10, 6))

    if log_scale:
        plt.loglog(sample_sizes, errors, 'o-', label=method_name)

        # Plot reference convergence rate
        N_ref = np.array([sample_sizes[0], sample_sizes[-1]])
        error_ref = errors[0] * (N_ref / sample_sizes[0]) ** (-reference_rate)
        plt.loglog(N_ref, error_ref, '--', label=f'N^{-reference_rate:.1f}')
    else:
        plt.plot(sample_sizes, errors, 'o-', label=method_name)

    plt.xlabel('Sample Size (N)')
    plt.ylabel('Error')
    plt.title(f'Convergence Analysis: {method_name}')
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def plot_option_prices_grid(S_range: np.ndarray, K: float, prices: np.ndarray,
                            option_type: str = 'Call', save_path: str = None):
    """
    Plot option prices as a function of spot price.

    Parameters
    ----------
    S_range : np.ndarray
        Range of spot prices
    K : float
        Strike price
    prices : np.ndarray
        Option prices for each spot price
    option_type : str
        Type of option ('Call' or 'Put')
    save_path : str, optional
        Path to save the plot
    """
    plt.figure(figsize=(10, 6))

    plt.plot(S_range, prices, 'b-', linewidth=2, label=f'{option_type} Price')

    # Plot intrinsic value
    if option_type.lower() == 'call':
        intrinsic = np.maximum(S_range - K, 0)
    else:
        intrinsic = np.maximum(K - S_range, 0)

    plt.plot(S_range, intrinsic, 'r--', linewidth=1, label='Intrinsic Value')

    plt.axvline(K, color='gray', linestyle=':', label=f'Strike K={K}')
    plt.xlabel('Spot Price (S)')
    plt.ylabel('Option Price')
    plt.title(f'{option_type} Option Price')
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def compare_mc_qmc(mc_results: dict, qmc_results: dict,
                   sample_sizes: np.ndarray) -> pd.DataFrame:
    """
    Compare Monte Carlo and Quasi-Monte Carlo results.

    Parameters
    ----------
    mc_results : dict
        Dictionary with 'prices' and optionally 'errors'
    qmc_results : dict
        Dictionary with 'prices' and optionally 'errors'
    sample_sizes : np.ndarray
        Array of sample sizes

    Returns
    -------
    pd.DataFrame
        Comparison table
    """
    df = pd.DataFrame({
        'N': sample_sizes,
        'MC Price': mc_results['prices'],
        'QMC Price': qmc_results['prices']
    })

    if 'errors' in mc_results and 'errors' in qmc_results:
        df['MC Error'] = mc_results['errors']
        df['QMC Error'] = qmc_results['errors']
        df['Error Ratio (MC/QMC)'] = df['MC Error'] / df['QMC Error']

    return df


def generate_option_parameters(n_samples: int = 1, seed: int = None) -> pd.DataFrame:
    """
    Generate random option parameters for testing.

    Parameters
    ----------
    n_samples : int
        Number of parameter sets to generate
    seed : int, optional
        Random seed

    Returns
    -------
    pd.DataFrame
        DataFrame with random option parameters
    """
    if seed is not None:
        np.random.seed(seed)

    params = pd.DataFrame({
        'S0': np.random.uniform(80, 120, n_samples),
        'K': np.random.uniform(90, 110, n_samples),
        'r': np.random.uniform(0.01, 0.10, n_samples),
        'delta': np.random.uniform(0.0, 0.05, n_samples),
        'sigma': np.random.uniform(0.15, 0.40, n_samples),
        'T': np.random.uniform(0.25, 2.0, n_samples)
    })

    return params


def fibonacci_sequence(n: int) -> np.ndarray:
    """
    Generate Fibonacci sequence up to n terms.

    Parameters
    ----------
    n : int
        Number of Fibonacci numbers to generate

    Returns
    -------
    np.ndarray
        Fibonacci sequence
    """
    if n <= 0:
        return np.array([])
    if n == 1:
        return np.array([1])

    fib = np.zeros(n, dtype=int)
    fib[0] = fib[1] = 1

    for i in range(2, n):
        fib[i] = fib[i-1] + fib[i-2]

    return fib
