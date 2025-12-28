"""
Tests for simulation utilities.
"""

import pytest
import numpy as np
from qmc_options import simulation


def test_box_muller():
    """Test Box-Muller transformation."""
    samples = simulation.box_muller(mu=0, sigma=1, size=1000)

    # Check mean and std are approximately correct
    assert np.abs(np.mean(samples)) < 0.1
    assert np.abs(np.std(samples) - 1.0) < 0.1


def test_gbm_explicit():
    """Test explicit GBM calculation."""
    S0 = 100
    r = 0.05
    sigma = 0.2
    delta = 0.02
    T = 1.0
    Z = np.random.randn(10)

    # Test at n=0
    S_0 = simulation.gbm_explicit(S0, r, sigma, delta, 0, T, Z)
    assert S_0 == S0

    # Test at n=5
    S_5 = simulation.gbm_explicit(S0, r, sigma, delta, 5, T, Z)
    assert S_5 > 0


def test_gbm_euler():
    """Test GBM using Euler discretization."""
    path = simulation.gbm_euler(
        S0=100, T=1.0, n=252,
        r=0.05, delta=0.02, sigma=0.2,
        seed=42
    )

    # Check path starts at S0
    assert path[0] == 100

    # Check all prices are positive
    assert np.all(path > 0)

    # Check path length
    assert len(path) == 252


def test_gbm_exact():
    """Test GBM using exact solution."""
    path = simulation.gbm_exact(
        S0=100, T=1.0, n=252,
        r=0.05, delta=0.02, sigma=0.2,
        Z=np.random.randn(252)
    )

    # Check path starts at S0
    assert np.isclose(path[0], 100)

    # Check all prices are positive
    assert np.all(path > 0)

    # Check path length (n+1 including S0)
    assert len(path) == 253


def test_generate_correlated_normals():
    """Test generation of correlated normal variables."""
    N = 10000
    rho = 0.7

    Z1, Z2 = simulation.generate_correlated_normals(N, rho)

    # Check means are approximately 0
    assert np.abs(np.mean(Z1)) < 0.1
    assert np.abs(np.mean(Z2)) < 0.1

    # Check correlation is approximately rho
    correlation = np.corrcoef(Z1, Z2)[0, 1]
    assert np.abs(correlation - rho) < 0.05


def test_qmc_to_normal():
    """Test transformation of QMC points to normal."""
    points = np.array([[0.1, 0.5, 0.9],
                       [0.3, 0.7, 0.2]])

    normals = simulation.qmc_to_normal(points)

    # Check shape
    assert normals.shape == points.shape

    # Check that 0.5 maps to approximately 0
    assert np.abs(normals[0, 1]) < 0.1


def test_periodize():
    """Test periodization transformation."""
    # Test at boundaries
    assert simulation.periodize(0.0) == 0.0
    assert simulation.periodize(1.0) == 0.0

    # Test at midpoint
    assert simulation.periodize(0.5) == 1.0

    # Test at 0.25
    assert simulation.periodize(0.25) == 0.5


def test_periodize_array():
    """Test array periodization."""
    points = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    result = simulation.periodize_array(points)

    expected = np.array([0.0, 0.5, 1.0, 0.5, 0.0])
    assert np.allclose(result, expected)


def test_standard_error():
    """Test standard error calculation."""
    samples = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    se = simulation.standard_error(samples)

    # Manual calculation
    expected_se = np.std(samples, ddof=1) / np.sqrt(5)
    assert np.isclose(se, expected_se)


def test_standard_error_single_sample():
    """Test standard error with single sample."""
    samples = np.array([1.0])
    se = simulation.standard_error(samples)
    assert se == 0.0
