# Quasi-Monte Carlo Methods for Stock Options Pricing

A Python package implementing Monte Carlo and Quasi-Monte Carlo methods for pricing exotic stock options, including spread options, Asian options, and lookback options.

**Originally developed in MATLAB/Octave, now fully migrated to Python.**

## Overview

This repository contains implementations of:

- **Quasi-random sequence generators**: Van der Corput, Halton, Good Lattice Points (GLP)
- **Option pricing methods**: European, Asian, Spread, and Lookback options
- **Greeks calculation**: Both pathwise and likelihood ratio methods
- **Analytical formulas**: Black-Scholes, Margrabe formula for validation

### Option Types

- **Vanilla options**: Standard European calls and puts (used for testing and reference)
- **Spread options**: Linear combinations of multiple underlying assets
- **Asian options**: Arithmetic average price options
- **Lookback options**: Path-dependent options tracking max/min prices at discrete monitoring points

## Installation

### From Source

```bash
git clone <repository-url>
cd quasi_monte_carlo_stock_options
pip install -e .
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Option Pricing

```python
import numpy as np
from qmc_options import generators, pricing, analytical

# Define option parameters
params = {
    'S0': 100.0,      # Initial stock price
    'K': 100.0,       # Strike price
    'r': 0.05,        # Risk-free rate
    'delta': 0.02,    # Dividend yield
    'sigma': 0.25,    # Volatility
    'T': 1.0          # Time to maturity
}

# Black-Scholes analytical price
bs_price = analytical.black_scholes_call(**params)
print(f"Black-Scholes Price: ${bs_price:.4f}")

# Monte Carlo pricing with Halton sequence
N = 10000
halton_points = generators.halton([2], N)[:, 0]
mc_price = pricing.european_call_mc(points=halton_points, **params)
print(f"MC Price: ${mc_price:.4f}")
```

### Spread Options

```python
# Generate Good Lattice Points
glp = generators.good_lattice_points(m=12)

# Price spread option
spread_price = pricing.spread_option(
    points=glp,
    w1=1.0, w2=1.0,
    r=0.05, K=0.0,
    S10=100, S20=105,
    delta1=0.03, delta2=0.04,
    sigma1=0.25, sigma2=0.20,
    rho12=0.7, T=1.0
)

# Compare with Margrabe formula (exact for K=0)
margrabe_price = analytical.margrabe_formula(
    S10=100, S20=105,
    delta1=0.03, delta2=0.04,
    sigma1=0.25, sigma2=0.20,
    rho12=0.7, T=1.0
)
```

### Greeks Calculation

```python
from qmc_options import greeks

# Analytical Greeks
delta = analytical.call_delta(**params)
gamma = analytical.call_gamma(**params)
vega = analytical.call_vega(**params)

# Monte Carlo Greeks (pathwise method)
mc_delta = greeks.pathwise_delta_european_call(points=halton_points, **params)
mc_vega = greeks.pathwise_vega_european_call(points=halton_points, **params)

# Likelihood ratio method
lr_delta = greeks.likelihood_delta_european_call(points=halton_points, **params)
```

## Package Structure

```
qmc_options/
├── __init__.py
├── generators.py      # Quasi-random sequence generators
├── simulation.py      # GBM simulation and MC utilities
├── analytical.py      # Black-Scholes and analytical formulas
├── pricing.py         # Option pricing functions
├── greeks.py          # Greeks calculation (pathwise & likelihood)
└── utils.py           # Utility functions and plotting

tests/
├── test_generators.py
├── test_analytical.py
├── test_simulation.py
└── test_pricing.py

notebooks/
├── 01_intro_qmc_sequences.ipynb
├── 02_option_pricing.ipynb
└── 03_greeks_analysis.ipynb
```

## Modules

### `generators`
- `van_der_corput(base, n)`: Van der Corput sequence
- `halton(primes, N)`: Halton sequence
- `good_lattice_points(m)`: GLP using Fibonacci numbers
- `random_shift(points)`: Random shift for variance reduction

### `analytical`
- `black_scholes_call(S0, K, r, delta, sigma, T)`: BS call formula
- `margrabe_formula(...)`: Spread option with K=0
- `call_delta(...)`, `call_gamma(...)`, etc.: Analytical Greeks

### `pricing`
- `european_call_mc(...)`: European call with MC/QMC
- `spread_option(...)`: Spread option pricing
- `asian_call(...)`: Asian call option
- `lookback_call(...)`, `lookback_put(...)`: Lookback options

### `greeks`
- Pathwise methods: `pathwise_delta_european_call(...)`, etc.
- Likelihood ratio methods: `likelihood_delta_european_call(...)`, etc.

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_generators.py

# Run with verbose output
pytest -v tests/
```

## Interactive Examples

Explore the Jupyter notebooks in the `notebooks/` directory:

1. **01_intro_qmc_sequences.ipynb**: Introduction to quasi-random sequences
2. **02_option_pricing.ipynb**: Option pricing examples and convergence analysis
3. **03_greeks_analysis.ipynb**: Greeks calculation and visualization

```bash
jupyter notebook notebooks/
```

## Key Features

- **Fast convergence**: QMC methods achieve O(N⁻¹) vs O(N⁻⁰·⁵) for standard MC
- **Multiple sequences**: Van der Corput, Halton, Good Lattice Points
- **Variance reduction**: Random shifts, periodization techniques
- **Comprehensive testing**: Full pytest suite with analytical validation
- **Educational**: Jupyter notebooks with visualizations

## Theory

### Quasi-Monte Carlo Integration

Standard Monte Carlo integration converges at rate O(N⁻⁰·⁵). QMC methods use low-discrepancy sequences instead of pseudo-random numbers, achieving convergence rates up to O(N⁻¹) for sufficiently smooth integrands.

### Greeks Estimation

Two main approaches:
- **Pathwise derivative**: Differentiate the payoff function (works for smooth payoffs)
- **Likelihood ratio**: Use score function (more general, higher variance)

## References

For detailed mathematical background, see the included PDF document:
`TFM-UNED-RubenColominaCitoler-VersionFinal-v4-2.pdf`

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Migration Notes

This project was originally implemented in MATLAB/Octave and has been fully migrated to Python with:
- Modern Python package structure
- Comprehensive type hints
- Full pytest test suite
- Interactive Jupyter notebooks
- Enhanced documentation

The original MATLAB code is preserved in the `src/` directory for reference.
