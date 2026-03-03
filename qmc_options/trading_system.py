"""
Automated trading system using quasi-Monte Carlo option pricing.

Trading strategies:
1. Market making: Provide liquidity, profit from bid-ask spread
2. Volatility arbitrage: Trade mispriced options
3. Delta hedging: Market-neutral positions
4. Statistical arbitrage: Mean reversion strategies
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


class OptionPosition:
    """Represents a single option position."""

    def __init__(self, ticker: str, strike: float, expiry: str,
                 option_type: str, quantity: int, entry_price: float):
        self.ticker = ticker
        self.strike = strike
        self.expiry = expiry
        self.option_type = option_type  # 'call' or 'put'
        self.quantity = quantity  # positive for long, negative for short
        self.entry_price = entry_price
        self.entry_time = datetime.now()

    def pnl(self, current_price: float) -> float:
        """Calculate P&L for this position."""
        return (current_price - self.entry_price) * self.quantity * 100  # Options contract multiplier


class Portfolio:
    """
    Manage portfolio of options and underlying stocks.
    """

    def __init__(self, initial_capital: float):
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.positions: List[OptionPosition] = []
        self.stock_positions: Dict[str, int] = {}  # ticker -> quantity
        self.trades_history: List[dict] = []

    def add_option_position(self, position: OptionPosition):
        """Add new option position."""
        self.positions.append(position)

        # Record trade
        self.trades_history.append({
            'time': datetime.now(),
            'type': 'option',
            'ticker': position.ticker,
            'strike': position.strike,
            'expiry': position.expiry,
            'option_type': position.option_type,
            'quantity': position.quantity,
            'price': position.entry_price
        })

    def add_stock_position(self, ticker: str, quantity: int, price: float):
        """Add stock position (for hedging)."""
        if ticker in self.stock_positions:
            self.stock_positions[ticker] += quantity
        else:
            self.stock_positions[ticker] = quantity

        # Update capital
        self.capital -= quantity * price

        # Record trade
        self.trades_history.append({
            'time': datetime.now(),
            'type': 'stock',
            'ticker': ticker,
            'quantity': quantity,
            'price': price
        })

    def calculate_portfolio_greeks(self, pricing_func) -> dict:
        """
        Calculate total portfolio Greeks.

        Parameters
        ----------
        pricing_func : callable
            Function that takes (ticker, strike, expiry) and returns (price, greeks)

        Returns
        -------
        dict
            {'delta': float, 'gamma': float, 'vega': float, 'theta': float}
        """
        total_greeks = {'delta': 0, 'gamma': 0, 'vega': 0, 'theta': 0}

        for position in self.positions:
            _, greeks = pricing_func(position.ticker, position.strike, position.expiry)

            # Scale by position size
            for greek in total_greeks:
                total_greeks[greek] += greeks[greek] * position.quantity

        # Add stock positions (delta = 1 per share)
        for ticker, quantity in self.stock_positions.items():
            total_greeks['delta'] += quantity

        return total_greeks

    def total_pnl(self, current_prices: dict) -> float:
        """
        Calculate total portfolio P&L.

        Parameters
        ----------
        current_prices : dict
            {'option_id': price, 'stock_ticker': price}
        """
        pnl = 0

        # Options P&L
        for i, position in enumerate(self.positions):
            current_price = current_prices.get(f'option_{i}', position.entry_price)
            pnl += position.pnl(current_price)

        # Stock P&L
        for ticker, quantity in self.stock_positions.items():
            if ticker in current_prices:
                pnl += quantity * (current_prices[ticker] - self.initial_capital / len(self.stock_positions))

        return pnl


class VolatilityArbitrageStrategy:
    """
    Trade options based on mispricing vs. model value.

    Strategy:
    1. Calculate fair value using QMC pricing
    2. Compare to market price
    3. If mispricing > threshold, trade
    4. Delta hedge the position
    5. Exit when mispricing corrects
    """

    def __init__(self, portfolio: Portfolio, pricing_model,
                 mispricing_threshold: float = 0.10):
        """
        Parameters
        ----------
        portfolio : Portfolio
            Trading portfolio
        pricing_model : object
            Calibrated pricing model (Heston, Merton, etc.)
        mispricing_threshold : float
            Trade if |model_price - market_price| / market_price > threshold
        """
        self.portfolio = portfolio
        self.pricing_model = pricing_model
        self.mispricing_threshold = mispricing_threshold

    def scan_opportunities(self, options_chain: pd.DataFrame,
                          S0: float, r: float, delta: float, T: float) -> List[dict]:
        """
        Scan options chain for mispriced options.

        Returns
        -------
        List[dict]
            Trading opportunities: [{'strike', 'type', 'market_price', 'model_price', 'edge'}]
        """
        opportunities = []

        for _, row in options_chain.iterrows():
            strike = row['strike']

            # Price call using model
            model_call_price = self.price_option(S0, strike, r, delta, T, 'call')

            # Check for mispricing
            market_call = row.get('call_price', 0)
            if market_call > 0:
                edge = (model_call_price - market_call) / market_call

                if abs(edge) > self.mispricing_threshold:
                    opportunities.append({
                        'strike': strike,
                        'type': 'call',
                        'market_price': market_call,
                        'model_price': model_call_price,
                        'edge': edge,
                        'action': 'buy' if edge > 0 else 'sell'
                    })

        # Sort by absolute edge
        opportunities.sort(key=lambda x: abs(x['edge']), reverse=True)

        return opportunities

    def price_option(self, S0: float, K: float, r: float, delta: float, T: float,
                    option_type: str) -> float:
        """Price option using calibrated model."""
        # This would call your Heston or Merton pricer
        # Placeholder implementation
        from qmc_options import analytical
        return analytical.black_scholes_call(S0, K, r, delta, 0.25, T)

    def execute_trade(self, opportunity: dict, ticker: str, expiry: str,
                     quantity: int = 1):
        """
        Execute a volatility arbitrage trade with delta hedge.

        Parameters
        ----------
        opportunity : dict
            From scan_opportunities()
        ticker : str
            Underlying ticker
        expiry : str
            Option expiration date
        quantity : int
            Number of contracts
        """
        # 1. Trade the option
        action_quantity = quantity if opportunity['action'] == 'buy' else -quantity

        position = OptionPosition(
            ticker=ticker,
            strike=opportunity['strike'],
            expiry=expiry,
            option_type=opportunity['type'],
            quantity=action_quantity,
            entry_price=opportunity['market_price']
        )

        self.portfolio.add_option_position(position)

        # 2. Delta hedge with stock
        # Calculate delta
        from qmc_options import analytical
        # Simplified - use model delta
        delta = 0.5  # Placeholder - calculate actual delta

        # Hedge shares = -delta * contracts * 100
        hedge_shares = -int(delta * action_quantity * 100)

        if hedge_shares != 0:
            from qmc_options.market_data import MarketDataFeed
            stock_price = MarketDataFeed.get_current_price(ticker)
            self.portfolio.add_stock_position(ticker, hedge_shares, stock_price)

        print(f"Executed {opportunity['action']} {abs(action_quantity)} contracts @ ${opportunity['market_price']:.2f}")
        print(f"Delta hedge: {'Buy' if hedge_shares > 0 else 'Sell'} {abs(hedge_shares)} shares")
        print(f"Expected edge: {opportunity['edge']*100:.1f}%")


class DeltaHedger:
    """
    Continuous delta hedging to maintain market-neutral portfolio.
    """

    def __init__(self, portfolio: Portfolio, rebalance_threshold: float = 0.1):
        """
        Parameters
        ----------
        portfolio : Portfolio
            Portfolio to hedge
        rebalance_threshold : float
            Rehedge when |delta| exceeds this threshold
        """
        self.portfolio = portfolio
        self.rebalance_threshold = rebalance_threshold
        self.hedging_history = []

    def calculate_required_hedge(self, pricing_func) -> dict:
        """
        Calculate required stock position to neutralize delta.

        Returns
        -------
        dict
            {'ticker': shares_to_trade}
        """
        greeks = self.portfolio.calculate_portfolio_greeks(pricing_func)
        current_delta = greeks['delta']

        # If delta is within threshold, no action needed
        if abs(current_delta) < self.rebalance_threshold * 100:
            return {}

        # Group by ticker (assuming single ticker for simplicity)
        # In production, handle multi-ticker portfolios
        hedge_trades = {}

        for position in self.portfolio.positions:
            ticker = position.ticker

            if ticker not in hedge_trades:
                hedge_trades[ticker] = 0

            # Calculate shares needed to offset option delta
            hedge_trades[ticker] -= int(current_delta)

        return hedge_trades

    def rebalance(self, pricing_func, current_prices: dict):
        """
        Execute delta rebalancing trades.

        Parameters
        ----------
        pricing_func : callable
            Pricing function for Greeks calculation
        current_prices : dict
            Current stock prices
        """
        required_hedges = self.calculate_required_hedge(pricing_func)

        for ticker, shares in required_hedges.items():
            if shares != 0:
                price = current_prices.get(ticker, 0)
                self.portfolio.add_stock_position(ticker, shares, price)

                self.hedging_history.append({
                    'time': datetime.now(),
                    'ticker': ticker,
                    'shares': shares,
                    'price': price
                })

                print(f"Rebalanced: {'Bought' if shares > 0 else 'Sold'} {abs(shares)} {ticker} @ ${price:.2f}")


class BacktestEngine:
    """
    Backtest trading strategies on historical data.
    """

    def __init__(self, strategy, start_date: str, end_date: str):
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.results = []

    def run(self, ticker: str) -> pd.DataFrame:
        """
        Run backtest.

        Returns
        -------
        pd.DataFrame
            Daily portfolio values, returns, Sharpe ratio, etc.
        """
        from qmc_options.market_data import MarketDataFeed

        # Fetch historical data
        prices = MarketDataFeed.get_historical_prices(ticker, self.start_date, self.end_date)

        daily_pnl = []
        portfolio_value = [self.strategy.portfolio.initial_capital]

        for date, row in prices.iterrows():
            # Simulate one day
            S0 = row['Close']

            # Strategy logic here
            # (Simplified - in production, fetch options chain for each day)

            # Calculate P&L
            current_prices = {ticker: S0}
            pnl = self.strategy.portfolio.total_pnl(current_prices)

            daily_pnl.append(pnl)
            portfolio_value.append(self.strategy.portfolio.initial_capital + pnl)

        # Calculate metrics
        results = pd.DataFrame({
            'date': prices.index,
            'portfolio_value': portfolio_value[:-1],
            'daily_pnl': daily_pnl
        })

        results['returns'] = results['portfolio_value'].pct_change()

        # Performance metrics
        total_return = (results['portfolio_value'].iloc[-1] / results['portfolio_value'].iloc[0] - 1) * 100
        sharpe_ratio = results['returns'].mean() / results['returns'].std() * np.sqrt(252)

        print(f"\n=== Backtest Results ===")
        print(f"Total Return: {total_return:.2f}%")
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
        print(f"Max Drawdown: {(results['portfolio_value'].min() / results['portfolio_value'].max() - 1) * 100:.2f}%")

        return results


# Example: Complete trading system
def live_trading_loop(ticker: str, strategy_type: str = 'volatility_arb',
                     initial_capital: float = 100000):
    """
    Main trading loop for live execution.

    Parameters
    ----------
    ticker : str
        Stock ticker to trade
    strategy_type : str
        'volatility_arb', 'market_making', or 'delta_neutral'
    initial_capital : float
        Starting capital
    """
    from qmc_options.market_data import MarketDataFeed, calibrate_model_from_market
    import time

    # Initialize
    portfolio = Portfolio(initial_capital)

    # Calibrate model
    print("Calibrating pricing model...")
    model_params = calibrate_model_from_market(ticker, '2024-06-21', 'heston')
    print(f"Calibrated Heston model: {model_params}")

    # Initialize strategy
    if strategy_type == 'volatility_arb':
        strategy = VolatilityArbitrageStrategy(portfolio, model_params)
    else:
        raise ValueError(f"Unknown strategy: {strategy_type}")

    # Initialize delta hedger
    hedger = DeltaHedger(portfolio, rebalance_threshold=0.1)

    print(f"\n=== Starting Live Trading ===")
    print(f"Ticker: {ticker}")
    print(f"Strategy: {strategy_type}")
    print(f"Initial Capital: ${initial_capital:,.0f}")

    # Main trading loop
    iteration = 0
    while True:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")

        try:
            # 1. Fetch current market data
            S0 = MarketDataFeed.get_current_price(ticker)
            r = MarketDataFeed.get_risk_free_rate()
            delta_div = MarketDataFeed.estimate_dividend_yield(ticker)

            # 2. Fetch options chain
            expiry = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            options_chain = MarketDataFeed.get_options_chain_yahoo(ticker, expiry)

            # 3. Scan for opportunities
            T = 30 / 365.0
            opportunities = strategy.scan_opportunities(options_chain, S0, r, delta_div, T)

            print(f"Found {len(opportunities)} trading opportunities")

            # 4. Execute best trade (if any)
            if opportunities and len(portfolio.positions) < 10:  # Position limit
                best_opp = opportunities[0]
                print(f"Best opportunity: {best_opp}")

                # Execute trade
                strategy.execute_trade(best_opp, ticker, expiry, quantity=1)

            # 5. Rebalance delta hedge
            # hedger.rebalance(pricing_func, {ticker: S0})

            # 6. Calculate P&L
            pnl = portfolio.total_pnl({ticker: S0})
            print(f"Current P&L: ${pnl:,.0f} ({pnl/initial_capital*100:.1f}%)")

            # 7. Risk management
            if pnl < -initial_capital * 0.20:  # 20% drawdown limit
                print("STOP LOSS TRIGGERED - Liquidating positions")
                break

        except Exception as e:
            print(f"Error: {e}")

        # Wait before next iteration (e.g., 1 minute)
        time.sleep(60)
