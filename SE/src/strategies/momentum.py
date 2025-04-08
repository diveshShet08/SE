import pandas as pd

class MomentumStrategy:
    def __init__(self, momentum_window=14):
        self.momentum_window = momentum_window

    def generate_signals(self, market_data: pd.DataFrame):
        """Generates buy/sell signals based on momentum."""
        market_data['momentum'] = market_data['close'].diff(self.momentum_window)
        market_data['signal'] = 0
        market_data.loc[market_data['momentum'] > 0, 'signal'] = 1  # Buy
        market_data.loc[market_data['momentum'] < 0, 'signal'] = -1  # Sell
        return market_data[['date', 'close', 'momentum', 'signal']]

