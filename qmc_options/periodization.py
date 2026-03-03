"""
Periodization transformations for variance reduction in QMC.

Periodization techniques smooth the integrand at boundaries,
improving convergence rates for quasi-Monte Carlo integration.
"""

import numpy as np


class PeriodicTransform:
    """
    Periodization transformations for [0,1] -> [0,1].

    Provides 8 different transformation types (polynomial and trigonometric)
    with their derivatives for change-of-variables in QMC integration.
    """

    @staticmethod
    def transform(t: np.ndarray, param: int) -> np.ndarray:
        """
        Apply periodization transformation.

        Parameters
        ----------
        t : np.ndarray
            Input values in [0, 1]
        param : int
            Transformation type:
            1-3: Polynomial (degrees 2, 3, 4)
            4-7: Trigonometric (various)
            8: Identity (no transformation)

        Returns
        -------
        np.ndarray
            Transformed values
        """
        if param == 1:  # poly-2
            return 3 * t**2 - 2 * t**3
        elif param == 2:  # poly-3
            return 10 * t**3 - 15 * t**4 + 6 * t**5
        elif param == 3:  # poly-4
            return 35 * t**4 - 84 * t**5 + 70 * t**6 - 20 * t**7
        elif param == 4:  # sin-1
            return 0.5 * (1 - np.cos(np.pi * t))
        elif param == 5:  # sin-2
            return (1 / (2 * np.pi)) * (2 * np.pi * t - np.sin(2 * np.pi * t))
        elif param == 6:  # sin-3
            return (1 / 16) * (8 - 9 * np.cos(np.pi * t) + np.cos(3 * np.pi * t))
        elif param == 7:  # sin-4
            return (1 / (12 * np.pi)) * (12 * np.pi * t - 8 * np.sin(2 * np.pi * t) +
                                         np.sin(4 * np.pi * t))
        elif param == 8:  # identity
            return t
        else:
            raise ValueError(f"Invalid periodization parameter: {param}. Must be 1-8.")

    @staticmethod
    def derivative(t: np.ndarray, param: int) -> np.ndarray:
        """
        Compute derivative of periodization transformation.

        Required for change-of-variables formula in QMC integration.

        Parameters
        ----------
        t : np.ndarray
            Input values in [0, 1]
        param : int
            Transformation type (1-8)

        Returns
        -------
        np.ndarray
            Derivative values
        """
        if param == 1:  # poly-2
            return 6 * t - 6 * t**2
        elif param == 2:  # poly-3
            return 30 * t**2 - 60 * t**3 + 30 * t**4
        elif param == 3:  # poly-4
            return 140 * t**3 - 420 * t**4 + 420 * t**5 - 140 * t**6
        elif param == 4:  # sin-1
            return (np.pi / 2) * np.sin(np.pi * t)
        elif param == 5:  # sin-2
            return 1 - np.cos(2 * np.pi * t)
        elif param == 6:  # sin-3
            return (1 / 16) * (9 * np.pi * np.sin(np.pi * t) -
                               3 * np.pi * np.sin(3 * np.pi * t))
        elif param == 7:  # sin-4
            return (1 / (12 * np.pi)) * (12 * np.pi - 16 * np.pi * np.cos(2 * np.pi * t) +
                                          4 * np.pi * np.cos(4 * np.pi * t))
        elif param == 8:  # identity
            return np.ones_like(t)
        else:
            raise ValueError(f"Invalid periodization parameter: {param}. Must be 1-8.")

    @staticmethod
    def apply_2d(points: np.ndarray, param: int) -> tuple:
        """
        Apply periodization to 2D point set with Jacobian.

        Parameters
        ----------
        points : np.ndarray
            Array of shape (N, 2) with points in [0, 1)^2
        param : int
            Periodization type

        Returns
        -------
        tuple
            (transformed_points, jacobian_determinant)
        """
        u1 = PeriodicTransform.transform(points[:, 0], param)
        u2 = PeriodicTransform.transform(points[:, 1], param)

        du1 = PeriodicTransform.derivative(points[:, 0], param)
        du2 = PeriodicTransform.derivative(points[:, 1], param)

        transformed = np.column_stack([u1, u2])
        jacobian = du1 * du2  # Diagonal Jacobian

        return transformed, jacobian


# Convenience functions for backward compatibility

def periodize(t: np.ndarray, param: int = 8) -> np.ndarray:
    """Apply periodization transformation."""
    return PeriodicTransform.transform(t, param)


def periodize_derivative(t: np.ndarray, param: int = 8) -> np.ndarray:
    """Compute periodization derivative."""
    return PeriodicTransform.derivative(t, param)


# Pre-defined transformation sets

POLYNOMIAL_TRANSFORMS = [1, 2, 3]  # Polynomial degrees 2, 3, 4
TRIGONOMETRIC_TRANSFORMS = [4, 5, 6, 7]  # Various trig transforms
ALL_TRANSFORMS = list(range(1, 9))


def compare_periodizations(integrand_func, points: np.ndarray,
                          transform_list: list = None) -> dict:
    """
    Compare different periodization methods on an integrand.

    Parameters
    ----------
    integrand_func : callable
        Function to integrate, takes 2D points as input
    points : np.ndarray
        QMC point set of shape (N, 2)
    transform_list : list, optional
        List of transformation types to compare. Default: all 8.

    Returns
    -------
    dict
        Results for each periodization method
    """
    if transform_list is None:
        transform_list = ALL_TRANSFORMS

    results = {}

    for param in transform_list:
        transformed, jacobian = PeriodicTransform.apply_2d(points, param)

        # Evaluate integrand on transformed points
        values = integrand_func(transformed)

        # Apply change of variables (multiply by Jacobian)
        integral_estimate = np.mean(values * jacobian)

        results[f'param_{param}'] = {
            'value': integral_estimate,
            'param': param,
            'name': _get_transform_name(param)
        }

    return results


def _get_transform_name(param: int) -> str:
    """Get descriptive name for transformation parameter."""
    names = {
        1: 'Polynomial (deg 2)',
        2: 'Polynomial (deg 3)',
        3: 'Polynomial (deg 4)',
        4: 'Trigonometric sin-1',
        5: 'Trigonometric sin-2',
        6: 'Trigonometric sin-3',
        7: 'Trigonometric sin-4',
        8: 'Identity (no transform)'
    }
    return names.get(param, 'Unknown')
