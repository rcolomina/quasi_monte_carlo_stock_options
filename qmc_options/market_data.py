"""
Market data integration for model calibration and real-time pricing.

Supports:
- Traditional markets: yfinance (stocks, ETFs, indices)
- Crypto (historical): CoinGecko, Binance
- Crypto (live): Pyth Network (for Solana)
- Options chain data
- Historical prices
- Implied volatility surfaces
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import warnings

try:
    import requests
    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False
    warnings.warn("requests not installed. Run: pip install requests")


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

    @staticmethod
    def fetch_crypto_coingecko(coin_id: str, days: int = 365) -> pd.DataFrame:
        """
        Fetch crypto data from CoinGecko API (free).

        Parameters
        ----------
        coin_id : str
            CoinGecko ID: "bitcoin", "ethereum", "solana", etc.
        days : int
            Number of days of history

        Returns
        -------
        DataFrame
            Columns: ['timestamp', 'price']
        """
        if not HAVE_REQUESTS:
            raise ImportError("Install requests: pip install requests")

        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily'
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'prices' not in data:
            raise ValueError(f"Failed to fetch {coin_id}: {data}")

        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        return df

    @staticmethod
    def fetch_crypto_binance(symbol: str, interval: str = "1d",
                            start_date: str = None, limit: int = 1000) -> pd.DataFrame:
        """
        Fetch crypto data from Binance API (free, high quality).

        Parameters
        ----------
        symbol : str
            Trading pair (e.g., "BTCUSDT", "SOLUSDT", "ETHUSDT")
        interval : str
            Candlestick interval: "1m", "5m", "1h", "1d", etc.
        start_date : str
            Start date "YYYY-MM-DD" (optional)
        limit : int
            Max number of candles (default 1000)

        Returns
        -------
        DataFrame
            OHLCV data
        """
        if not HAVE_REQUESTS:
            raise ImportError("Install requests: pip install requests")

        url = "https://api.binance.com/api/v3/klines"

        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }

        if start_date:
            start_ts = int(pd.Timestamp(start_date).timestamp() * 1000)
            params['startTime'] = start_ts

        response = requests.get(url, params=params)
        data = response.json()

        if not isinstance(data, list):
            raise ValueError(f"Binance API error: {data}")

        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df[['open', 'high', 'low', 'close', 'volume']] = \
            df[['open', 'high', 'low', 'close', 'volume']].astype(float)

        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]


def calculate_historical_volatility(prices, window: int = 30, trading_days: int = 252) -> float:
    """
    Calculate historical volatility (annualized).

    Parameters
    ----------
    prices : pd.Series or np.ndarray
        Daily closing prices
    window : int
        Rolling window in days
    trading_days : int
        Trading days per year (252 for stocks, 365 for crypto)

    Returns
    -------
    float
        Annualized historical volatility
    """
    if isinstance(prices, pd.Series):
        returns = np.log(prices / prices.shift(1)).dropna().values
    else:
        returns = np.diff(np.log(prices))

    if len(returns) < window:
        window = len(returns)

    recent_returns = returns[-window:]
    volatility = np.std(recent_returns) * np.sqrt(trading_days)

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


def calibrate_asset_from_ticker(ticker: str,
                               lookback_days: int = 365,
                               asset_type: str = "auto") -> Dict:
    """
    Complete calibration pipeline from ticker to model parameters.

    Parameters
    ----------
    ticker : str
        "AAPL" for stocks, "solana" for crypto (CoinGecko), "BTCUSDT" for Binance
    lookback_days : int
        Historical data window
    asset_type : str
        "stock", "crypto_coingecko", "crypto_binance", or "auto" (detect)

    Returns
    -------
    dict
        Complete calibration results with characteristics and parameters

    Examples
    --------
    >>> # Calibrate Apple stock
    >>> result = calibrate_asset_from_ticker("AAPL", lookback_days=365)
    >>> print(f"Model: {result['model']}, Vol: {result['characteristics'].volatility:.2%}")

    >>> # Calibrate Solana
    >>> result = calibrate_asset_from_ticker("solana", asset_type="crypto_coingecko")
    >>> print(f"Recommended: {result['model']}")

    >>> # Calibrate Bitcoin from Binance
    >>> result = calibrate_asset_from_ticker("BTCUSDT", asset_type="crypto_binance")
    """
    from qmc_options.calibration import AssetAnalyzer, ModelCalibrator

    # Auto-detect asset type
    if asset_type == "auto":
        if ticker.endswith("USDT"):
            asset_type = "crypto_binance"
        elif len(ticker) <= 5 and ticker.isupper():
            asset_type = "stock"
        else:
            asset_type = "crypto_coingecko"

    # Fetch data
    print(f"📊 Fetching {lookback_days} days of data for {ticker}...")

    if asset_type == "stock":
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        data = MarketDataFeed.get_historical_prices(ticker, start_date, end_date)
        prices = data['Close'].values
        trading_days = 252

    elif asset_type == "crypto_coingecko":
        data = MarketDataFeed.fetch_crypto_coingecko(ticker, days=lookback_days)
        prices = data['price'].values
        trading_days = 365

    elif asset_type == "crypto_binance":
        start_date = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        data = MarketDataFeed.fetch_crypto_binance(ticker, interval="1d",
                                                   start_date=start_date)
        prices = data['close'].values
        trading_days = 365

    else:
        raise ValueError(f"Unknown asset_type: {asset_type}")

    print(f"✅ Fetched {len(prices)} days")

    # Analyze characteristics
    print(f"🔍 Analyzing characteristics...")
    analyzer = AssetAnalyzer(ticker)
    characteristics = analyzer.analyze(prices, trading_days_per_year=trading_days)
    print(characteristics)

    # Calibrate model
    print(f"\n⚙️  Calibrating {characteristics.recommended_model.upper()}...")
    calibrator = ModelCalibrator(characteristics)

    if characteristics.recommended_model == "heston":
        params = calibrator.calibrate_heston(prices)
    elif characteristics.recommended_model == "merton":
        params = calibrator.calibrate_merton(prices)
    elif characteristics.recommended_model == "bates":
        params = calibrator.calibrate_bates(prices)
    else:  # black_scholes
        params = {'sigma': characteristics.volatility}

    print(f"✅ Calibration complete!")

    return {
        'ticker': ticker,
        'characteristics': characteristics,
        'model': characteristics.recommended_model,
        'parameters': params,
        'current_price': float(prices[-1]),
        'trading_days': trading_days,
        'data': data
    }
