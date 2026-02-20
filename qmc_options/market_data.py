"""
Market data integration for model calibration and real-time pricing.

Supports:
- Options chain data
- Historical prices
- Implied volatility surfaces
- Real-time feeds
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class MarketDataFeed:
    """
    Interface for market data (implement with your provider).

    Providers:
    - Free: Yahoo Finance, Alpha Vantage
    - Premium: Interactive Brokers, TD Ameritrade API
    - Professional: Bloomberg, Refinitiv
    """

    @staticmethod
    def get_options_chain_yahoo(ticker: str, expiration_date: str = None) -> pd.DataFrame:
        """
        Fetch options chain from Yahoo Finance (FREE).

        Example:
            df = MarketDataFeed.get_options_chain_yahoo('SPY', '2024-03-15')

        Returns
        -------
        pd.DataFrame
            Columns: strike, call_price, put_price, call_iv, put_iv, volume, oi
        """
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("Install yfinance: pip install yfinance")

        ticker_obj = yf.Ticker(ticker)
        options = ticker_obj.option_chain(expiration_date)

        # Combine calls and puts
        calls = options.calls[['strike', 'lastPrice', 'impliedVolatility', 'volume', 'openInterest']]
        puts = options.puts[['strike', 'lastPrice', 'impliedVolatility', 'volume', 'openInterest']]

        calls.columns = ['strike', 'call_price', 'call_iv', 'call_volume', 'call_oi']
        puts.columns = ['strike', 'put_price', 'put_iv', 'put_volume', 'put_oi']

        df = pd.merge(calls, puts, on='strike', how='outer')

        return df

    @staticmethod
    def get_historical_prices(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch historical stock prices.

        Returns
        -------
        pd.DataFrame
            Columns: date, open, high, low, close, volume
        """
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("Install yfinance: pip install yfinance")

        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(start=start_date, end=end_date)

        return df

    @staticmethod
    def get_current_price(ticker: str) -> float:
        """Get current stock price."""
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("Install yfinance: pip install yfinance")

        ticker_obj = yf.Ticker(ticker)
        return ticker_obj.info['currentPrice']

    @staticmethod
    def estimate_dividend_yield(ticker: str) -> float:
        """Estimate annualized dividend yield."""
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("Install yfinance: pip install yfinance")

        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info

        if 'dividendYield' in info and info['dividendYield']:
            return info['dividendYield']

        return 0.0

    @staticmethod
    def get_risk_free_rate() -> float:
        """
        Get current risk-free rate (10-year Treasury).

        In production, fetch from FRED API or Bloomberg.
        """
        # Placeholder - in production, fetch from API
        # https://fred.stlouisfed.org/series/DGS10
        return 0.04  # 4% default


def calculate_historical_volatility(prices: pd.Series, window: int = 30) -> float:
    """
    Calculate historical volatility (annualized).

    Parameters
    ----------
    prices : pd.Series
        Daily closing prices
    window : int
        Rolling window in days

    Returns
    -------
    float
        Annualized historical volatility
    """
    returns = np.log(prices / prices.shift(1)).dropna()

    if len(returns) < window:
        window = len(returns)

    volatility = returns.tail(window).std() * np.sqrt(252)

    return volatility


def estimate_jump_parameters_from_history(prices: pd.Series,
                                          threshold: float = 3.0) -> dict:
    """
    Estimate jump-diffusion parameters from historical data.

    Identifies "jumps" as returns exceeding threshold * daily_volatility.

    Parameters
    ----------
    prices : pd.Series
        Daily closing prices
    threshold : float
        Number of standard deviations to classify as jump

    Returns
    -------
    dict
        {'lambda_jump': float, 'mu_jump': float, 'sigma_jump': float}
    """
    returns = np.log(prices / prices.shift(1)).dropna()

    # Estimate continuous volatility
    daily_vol = returns.std()

    # Identify jumps
    jump_threshold = threshold * daily_vol
    jumps = returns[abs(returns) > jump_threshold]

    # Jump intensity (jumps per year)
    lambda_jump = len(jumps) / (len(returns) / 252)

    if len(jumps) > 0:
        mu_jump = jumps.mean()
        sigma_jump = jumps.std()
    else:
        mu_jump = 0.0
        sigma_jump = 0.1

    return {
        'lambda_jump': lambda_jump,
        'mu_jump': mu_jump,
        'sigma_jump': sigma_jump,
        'n_jumps_detected': len(jumps),
        'continuous_vol': daily_vol * np.sqrt(252)
    }


def build_iv_surface(options_chain: pd.DataFrame, S0: float) -> np.ndarray:
    """
    Build implied volatility surface from options chain.

    Parameters
    ----------
    options_chain : pd.DataFrame
        Options data with columns: strike, call_iv, put_iv
    S0 : float
        Current stock price

    Returns
    -------
    np.ndarray
        IV surface data for calibration
    """
    # Filter for liquid options (high volume/OI)
    liquid = options_chain[
        (options_chain['call_volume'] > 10) |
        (options_chain['put_volume'] > 10)
    ].copy()

    # Calculate moneyness
    liquid['moneyness'] = liquid['strike'] / S0

    # Average call and put IVs
    liquid['avg_iv'] = (liquid['call_iv'] + liquid['put_iv']) / 2

    return liquid[['strike', 'moneyness', 'avg_iv']].values


# Example: Complete calibration workflow
def calibrate_model_from_market(ticker: str, expiration_date: str,
                                model_type: str = 'heston') -> dict:
    """
    Full calibration workflow: fetch data → calibrate → return parameters.

    Parameters
    ----------
    ticker : str
        Stock ticker (e.g., 'SPY', 'AAPL')
    expiration_date : str
        Option expiration (e.g., '2024-03-15')
    model_type : str
        'heston', 'merton', or 'kou'

    Returns
    -------
    dict
        Calibrated model parameters
    """
    from qmc_options import stochastic_volatility, jump_diffusion

    # 1. Fetch current market data
    S0 = MarketDataFeed.get_current_price(ticker)
    r = MarketDataFeed.get_risk_free_rate()
    delta = MarketDataFeed.estimate_dividend_yield(ticker)

    # 2. Fetch options chain
    options = MarketDataFeed.get_options_chain_yahoo(ticker, expiration_date)

    # 3. Calculate time to maturity
    T = (pd.to_datetime(expiration_date) - datetime.now()).days / 365.0

    # 4. Prepare market data for calibration
    market_data = []
    for _, row in options.iterrows():
        if pd.notna(row['call_price']) and row['call_price'] > 0.01:
            market_data.append({
                'K': row['strike'],
                'T': T,
                'price': row['call_price']
            })

    # 5. Calibrate model
    if model_type == 'heston':
        params = stochastic_volatility.calibrate_heston_to_surface(
            S0, r, delta, market_data
        )
    elif model_type == 'merton':
        params = jump_diffusion.calibrate_merton_to_market(
            S0, r, delta, T, market_data
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    # 6. Add market context
    params['ticker'] = ticker
    params['S0'] = S0
    params['r'] = r
    params['delta'] = delta
    params['calibration_date'] = datetime.now().isoformat()

    return params
