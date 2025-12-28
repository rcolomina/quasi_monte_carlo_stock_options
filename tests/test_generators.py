"""
Tests for quasi-random sequence generators.
"""

import pytest
import numpy as np
from qmc_options import generators


def test_van_der_corput():
    """Test Van der Corput sequence generation."""
    # Test first few values in base 2
    assert generators.van_der_corput(2, 1) == 0.5
    assert generators.van_der_corput(2, 2) == 0.25
    assert generators.van_der_corput(2, 3) == 0.75

    # Test base 3
    result = generators.van_der_corput(3, 1)
    assert 0 <= result < 1


def test_halton_sequence():
    """Test Halton sequence generation."""
    primes = [2, 3]
    N = 10
    sequence = generators.halton(primes, N)

    # Check shape
    assert sequence.shape == (N, 2)

    # Check all values in [0, 1)
    assert np.all(sequence >= 0)
    assert np.all(sequence < 1)


def test_good_lattice_points():
    """Test Good Lattice Points generation."""
    m = 6  # Should give fibo(6) = 8 points
    glp = generators.good_lattice_points(m)

    # Check shape
    assert glp.shape[1] == 2  # 2D
    assert glp.shape[0] == 8  # fibo(6) = 8

    # Check all values in [0, 1)
    assert np.all(glp >= 0)
    assert np.all(glp < 1)


def test_good_lattice_points_nd():
    """Test n-dimensional Good Lattice Points."""
    N = 100
    dim = 3
    glp = generators.good_lattice_points_nd(N, dim)

    # Check shape
    assert glp.shape == (N, dim)

    # Check all values in [0, 1)
    assert np.all(glp >= 0)
    assert np.all(glp < 1)


def test_random_shift():
    """Test random shift of quasi-random points."""
    points = np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])
    shifted = generators.random_shift(points)

    # Check shape preserved
    assert shifted.shape == points.shape

    # Check all values still in [0, 1)
    assert np.all(shifted >= 0)
    assert np.all(shifted < 1)


def test_random_permutation():
    """Test random permutation of coordinates."""
    points = np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])
    permuted = generators.random_permutation(points)

    # Check shape preserved
    assert permuted.shape == points.shape

    # Check values are from original set (in some order)
    for col in range(points.shape[1]):
        assert set(np.round(permuted[:, col], 5)) == set(np.round(points[:, col], 5))
