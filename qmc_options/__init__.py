"""
Quasi-Monte Carlo Methods for Stock Options Pricing

A Python package implementing Monte Carlo and Quasi-Monte Carlo methods
for pricing exotic stock options including spread, Asian, and lookback options.
"""

__version__ = "0.3.0"

from . import generators
from . import simulation
from . import analytical
from . import pricing
from . import greeks
from . import utils
from . import periodization
from . import spread_greeks
from . import jump_diffusion
from . import stochastic_volatility
from . import market_data
from . import trading_system

__all__ = [
    "generators",
    "simulation",
    "analytical",
    "pricing",
    "greeks",
    "utils",
    "periodization",
    "spread_greeks",
    "jump_diffusion",
    "stochastic_volatility",
    "market_data",
    "trading_system",
]
