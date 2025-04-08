import pandas as pd

class MeanReversionStrategy:
    def __init__(self, window=20):
        """Initialize with moving average window size."""
        self.window = window

    def generate_signals(self, market_data: pd.DataFrame):
        """Generates buy/sell signals."""
        market_data['sma'] = market_data['close'].rolling(window=self.window).mean()
        market_data['signal'] = 0
        market_data.loc[market_data['close'] < market_data['sma'], 'signal'] = 1  # Buy
        market_data.loc[market_data['close'] > market_data['sma'], 'signal'] = -1  # Sell
        return market_data[['date', 'close', 'sma', 'signal']]

