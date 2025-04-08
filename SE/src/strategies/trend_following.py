class TrendFollowingStrategy:
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, market_data: pd.DataFrame):
        """Detects uptrends/downtrends using moving averages."""
        market_data['short_ma'] = market_data['close'].rolling(self.short_window).mean()
        market_data['long_ma'] = market_data['close'].rolling(self.long_window).mean()
        market_data['signal'] = 0
        market_data.loc[market_data['short_ma'] > market_data['long_ma'], 'signal'] = 1  # Buy
        market_data.loc[market_data['short_ma'] < market_data['long_ma'], 'signal'] = -1  # Sell
        return market_data[['date', 'close', 'short_ma', 'long_ma', 'signal']]

