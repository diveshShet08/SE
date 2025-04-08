import pandas as pd
from .base_strategy import BaseStrategy

class BollingerBandsStrategy(BaseStrategy):
    """Bollinger Bands-based trading strategy."""

    def __init__(self, window=20, std_factor=2):
        """
        :param window: Rolling window size for SMA calculation.
        :param std_factor: Multiplication factor for standard deviation.
        """
        super().__init__(name="BollingerBandsStrategy")
        self.window = window
        self.std_factor = std_factor

    def generate_signals(self):
        """Calculates Bollinger Bands and generates buy/sell signals."""
        if self.data is None:
            raise ValueError("Market data not loaded. Use load_data() first.")

        # Compute moving average and standard deviation
        self.data['sma'] = self.data['close'].rolling(window=self.window).mean()
        self.data['std'] = self.data['close'].rolling(window=self.window).std()

        # Compute upper and lower Bollinger Bands
        self.data['upper_band'] = self.data['sma'] + (self.data['std'] * self.std_factor)
        self.data['lower_band'] = self.data['sma'] - (self.data['std'] * self.std_factor)

        # Generate signals
        self.data['signal'] = 0  # Default to no action
        self.data.loc[self.data['close'] < self.data['lower_band'], 'signal'] = 1  # Buy
        self.data.loc[self.data['close'] > self.data['upper_band'], 'signal'] = -1  # Sell

        return self.data[['date', 'close', 'sma', 'upper_band', 'lower_band', 'signal']]

