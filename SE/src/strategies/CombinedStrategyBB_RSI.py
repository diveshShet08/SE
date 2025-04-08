import pandas as pd
import numpy as np

class CombinedStrategyBB_RSI:
    def __init__(self, bollinger_period=20, bollinger_std=2.0, rsi_period=14, 
                 rsi_oversold=30, rsi_overbought=70, atr_period=14, 
                 sl_atr_multiplier=1.5, tp_type="ob", max_sl_pips=30):
        self.bollinger_period = int(bollinger_period)
        self.bollinger_std = float(bollinger_std)
        self.rsi_period = int(rsi_period)
        self.rsi_oversold = int(rsi_oversold)
        self.rsi_overbought = int(rsi_overbought)
        self.atr_period = int(atr_period)   
        self.sl_atr_multiplier = float(sl_atr_multiplier)
        self.tp_type = tp_type
        self.max_sl_pips = int(max_sl_pips)

    def calculate_indicators(self, data):
        """Calculates Bollinger Bands, RSI, and ATR."""
        data['SMA'] = data['Close'].rolling(window=self.bollinger_period).mean()
        data['STD'] = data['Close'].rolling(window=self.bollinger_period).std()
        data['UpperBand'] = data['SMA'] + (self.bollinger_std * data['STD'])
        data['LowerBand'] = data['SMA'] - (self.bollinger_std * data['STD'])
        
        delta = data['Close'].diff(1)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=self.rsi_period).mean()
        avg_loss = pd.Series(loss).rolling(window=self.rsi_period).mean()
        rs = avg_gain / (avg_loss + 1e-10)  # Avoid division by zero
        data['RSI'] = 100 - (100 / (1 + rs))
        
        data['ATR'] = data['High'].rolling(self.atr_period).max() - data['Low'].rolling(self.atr_period).min()
        return data
    
    def generate_signals(self, data):
        """Generates trade signals based on Bollinger Bands and RSI."""
        data = self.calculate_indicators(data)
        signals = []
        
        for i in range(1, len(data)):
            row = data.iloc[i]
            prev_row = data.iloc[i-1]
            
            atr_value = row['ATR'] * self.sl_atr_multiplier
            max_sl = self.max_sl_pips / 10000  # Convert pips to price
            sl_distance = min(atr_value, max_sl)
            
            if row['Close'] <= row['LowerBand'] and row['RSI'] <= self.rsi_oversold:
                entry_price = row['Close']
                sl = entry_price - sl_distance
                tp = row['UpperBand'] if self.tp_type == "ob" else entry_price + sl_distance * 2
                signals.append({'row':i,'type': 'BUY', 'price': entry_price, 'sl': sl, 'tp': tp})
                
            elif row['Close'] >= row['UpperBand'] and row['RSI'] >= self.rsi_overbought:
                entry_price = row['Close']
                sl = entry_price + sl_distance
                tp = row['LowerBand'] if self.tp_type == "opposite_band" else entry_price - sl_distance * 2
                signals.append({'row':i,'type': 'SELL', 'price': entry_price, 'sl': sl, 'tp': tp})
        
        return signals
