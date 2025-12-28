"""
Quasi-random sequence generators for Monte Carlo simulation.

This module implements various low-discrepancy sequences:
- Van der Corput sequence
- Halton sequence
- Good Lattice Points (GLP)
"""

import numpy as np


def van_der_corput(base: int, n: int) -> float:
    """
    Generate the n-th element of the Van der Corput sequence in given base.

    Parameters
    ----------
    base : int
        The base for the sequence (typically a prime number)
    n : int
        The index of the element to generate (1-indexed)

    Returns
    -------
    float
        The n-th Van der Corput number in [0, 1)
    """
    result = 0.0
    f = 1.0 / base
    i = n

    while i > 0:
        result += f * (i % base)
        i //= base
        f /= base

    return result


def halton(primes: list, N: int) -> np.ndarray:
    """
    Generate a Halton sequence of N points in s-dimensional space.

    Parameters
    ----------
    primes : list of int
        List of coprime bases (typically prime numbers) for each dimension
    N : int
        Number of points to generate

    Returns
    -------
    np.ndarray
        Array of shape (N, len(primes)) containing the Halton sequence
    """
    s = len(primes)
    sequence = np.zeros((N, s))

    for i in range(N):
        for j in range(s):
            sequence[i, j] = van_der_corput(primes[j], i + 1)

    return sequence


def good_lattice_points(m: int) -> np.ndarray:
    """
    Generate Good Lattice Points using Fibonacci numbers.

    This implementation generates a 2D lattice using Fibonacci sequence
    to determine the number of points and the generating vector.

    Parameters
    ----------
    m : int
        Fibonacci index (m >= 3). The number of points will be fibo(m)

    Returns
    -------
    np.ndarray
        Array of shape (N, 2) containing GLP in [0, 1)^2
        where N = fibonacci(m)
    """
    # Generate Fibonacci sequence
    fibo = np.zeros(m, dtype=int)
    fibo[0] = fibo[1] = 1

    for i in range(2, m):
        fibo[i] = fibo[i-1] + fibo[i-2]

    N = fibo[m-1]
    glp = np.zeros((N, 2))

    # Generating vector
    z = np.array([1, fibo[m-2]])

    for i in range(N):
        glp[i, 0] = ((i + 1) * z[0] / N) % 1.0
        glp[i, 1] = ((i + 1) * z[1] / N) % 1.0

    return glp


def good_lattice_points_nd(N: int, dim: int, z: np.ndarray = None) -> np.ndarray:
    """
    Generate Good Lattice Points in arbitrary dimensions.

    Parameters
    ----------
    N : int
        Number of points to generate
    dim : int
        Dimension of the space
    z : np.ndarray, optional
        Generating vector of length dim. If None, a default vector is used.

    Returns
    -------
    np.ndarray
        Array of shape (N, dim) containing GLP in [0, 1)^dim
    """
    if z is None:
        # Default generating vector (can be optimized)
        z = np.arange(1, dim + 1)

    glp = np.zeros((N, dim))

    for i in range(N):
        for j in range(dim):
            glp[i, j] = ((i + 1) * z[j] / N) % 1.0

    return glp


def random_shift(points: np.ndarray) -> np.ndarray:
    """
    Apply random shift to a set of quasi-random points.

    This technique can improve the variance reduction properties
    of quasi-Monte Carlo methods.

    Parameters
    ----------
    points : np.ndarray
        Array of shape (N, dim) containing points in [0, 1)^dim

    Returns
    -------
    np.ndarray
        Randomly shifted points, still in [0, 1)^dim
    """
    dim = points.shape[1]
    shift = np.random.rand(dim)
    return (points + shift) % 1.0


def random_permutation(points: np.ndarray) -> np.ndarray:
    """
    Apply random permutation to coordinates of quasi-random points.

    Parameters
    ----------
    points : np.ndarray
        Array of shape (N, dim) containing points

    Returns
    -------
    np.ndarray
        Points with randomly permuted coordinates
    """
    N, dim = points.shape
    result = points.copy()

    for j in range(dim):
        result[:, j] = np.random.permutation(result[:, j])

    return result
