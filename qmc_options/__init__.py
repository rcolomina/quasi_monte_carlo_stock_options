"""
Quasi-Monte Carlo Methods for Stock Options Pricing

A Python package implementing Monte Carlo and Quasi-Monte Carlo methods
for pricing exotic stock options including spread, Asian, and lookback options.
"""

__version__ = "0.1.0"

from . import generators
from . import simulation
from . import analytical
from . import pricing
from . import greeks
from . import utils

__all__ = [
    "generators",
    "simulation",
    "analytical",
    "pricing",
    "greeks",
    "utils",
]
