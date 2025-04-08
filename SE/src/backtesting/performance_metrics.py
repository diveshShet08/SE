import numpy as np
import pandas as pd

class PerformanceMetrics:
    def __init__(self, trades: pd.DataFrame = None, initial_balance: float = 10000):
        self.trades = trades if trades is not None else pd.DataFrame(columns=['timestamp', 'symbol', 'entry_price', 'exit_price', 'quantity', 'side', 'profit_loss'])
# class PerformanceMetrics:
#     def __init__(self, trades: pd.DataFrame, initial_balance: float = 10000):
        """
        trades: DataFrame containing columns ['timestamp', 'symbol', 'entry_price', 'exit_price', 'quantity', 'side', 'profit_loss']
        initial_balance: Starting capital for calculating returns
        """
        self.trades = trades
        self.trades['profit_loss'] = pd.to_numeric(self.trades['profit_loss'], errors='coerce').fillna(0)
        self.initial_balance = initial_balance
        self.equity_curve = self.calculate_equity_curve()

    def calculate_equity_curve(self):
        """Generates an equity curve from trade results."""
        if self.trades.empty:
            return pd.Series([self.initial_balance], index=['End'])  # Return initial balance only
        
        equity = [self.initial_balance]
        for pnl in self.trades['profit_loss']:
            equity.append(equity[-1] + pnl)
        return pd.Series(equity, index=self.trades['timestamp'].tolist() + ['End'])

    def total_return(self):
        """Calculates total return of the strategy."""
        return (self.equity_curve.iloc[-1] - self.initial_balance) / self.initial_balance
    
    def max_drawdown(self):
        """Calculates maximum drawdown."""
        peak = self.equity_curve.cummax()
        drawdown = self.equity_curve - peak
        return drawdown.min() / peak.max()
    
    def sharpe_ratio(self, risk_free_rate=0.0):
        """Computes Sharpe Ratio assuming daily returns."""
        returns = self.equity_curve.pct_change().dropna()
        return (returns.mean() - risk_free_rate) / returns.std()
    
    def win_rate(self):
        """Calculates win rate of trades."""
        wins = self.trades[self.trades['profit_loss'] > 0]
        return len(wins) / len(self.trades)
    
    def profit_factor(self):
        """Computes Profit Factor (sum of wins / sum of losses)."""
        gains = self.trades[self.trades['profit_loss'] > 0]['profit_loss'].sum()
        losses = abs(self.trades[self.trades['profit_loss'] < 0]['profit_loss'].sum())
        return gains / losses if losses > 0 else np.inf
    
    def calculate(self, trade_results):
        """Computes all key metrics and returns a performance report."""
        if not trade_results:
            return {
                'Total Return': 0,
                'Max Drawdown': 0,
                'Sharpe Ratio': 0,
                'Win Rate': 0,
                'Profit Factor': 0,
                'Expectancy': 0
            }

        self.trades = pd.DataFrame(trade_results)  # Update trades DataFrame
        self.trades['profit_loss'] = pd.to_numeric(self.trades['profit_loss'], errors='coerce').fillna(0)
        self.equity_curve = self.calculate_equity_curve()

        return self.trade_analysis_report()

    def expectancy(self):
        """Calculates trade expectancy."""
        return self.trades['profit_loss'].mean()
    
    def trade_analysis_report(self):
        """Returns a summary of key performance metrics."""
        return {
            'Total Return': self.total_return(),
            'Max Drawdown': self.max_drawdown(),
            'Sharpe Ratio': self.sharpe_ratio(),
            'Win Rate': self.win_rate(),
            'Profit Factor': self.profit_factor(),
            'Expectancy': self.expectancy()
        }


# import numpy as np
# import pandas as pd

# class PerformanceMetrics:
#     def __init__(self, trade_results: pd.DataFrame):
#         """
#         trade_results: DataFrame containing ['returns', 'equity_curve']
#         """
#         self.trade_results = trade_results

#     def sharpe_ratio(self, risk_free_rate=0.02):
#         """Calculate the Sharpe Ratio."""
#         excess_returns = self.trade_results['returns'] - risk_free_rate
#         return np.mean(excess_returns) / np.std(excess_returns)

#     def max_drawdown(self):
#         """Calculate Max Drawdown."""
#         equity_curve = self.trade_results['equity_curve']
#         peak = equity_curve.cummax()
#         drawdown = (equity_curve - peak) / peak
#         return drawdown.min()

#     def profit_factor(self):
#         """Calculate Profit Factor = (Total Profit / Total Loss)."""
#         profits = self.trade_results[self.trade_results['returns'] > 0]['returns'].sum()
#         losses = abs(self.trade_results[self.trade_results['returns'] < 0]['returns'].sum())
#         return profits / losses if losses > 0 else np.inf

#     def win_rate(self):
#         """Calculate Win Rate %."""
#         total_trades = len(self.trade_results)
#         winning_trades = len(self.trade_results[self.trade_results['returns'] > 0])
#         return (winning_trades / total_trades) * 100 if total_trades > 0 else 0


