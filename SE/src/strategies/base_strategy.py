import pandas as pd
from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """Abstract base class for all trading strategies."""
    
    def __init__(self, name="BaseStrategy"):
        self.name = name
        self.data = None

    def load_data(self, market_data: pd.DataFrame):
        """Loads market data into the strategy."""
        self.data = market_data

    @abstractmethod
    def generate_signals(self):
        """Each strategy must implement this method to return buy/sell signals."""
        pass

    def apply_risk_management(self, signals_df: pd.DataFrame):
        """Applies basic stop-loss & take-profit logic."""
        if "signal" not in signals_df.columns:
            raise ValueError("Signals DataFrame must contain a 'signal' column.")

        signals_df['stop_loss'] = signals_df['close'] * 0.98  # Example: 2% stop loss
        signals_df['take_profit'] = signals_df['close'] * 1.05  # Example: 5% take profit
        return signals_df

