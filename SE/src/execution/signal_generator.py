import MetaTrader5 as mt5

def check_signal(symbol: str, timeframe: str):
    # Example strategy: Simple 2-period Moving Average Crossover
    # Load the last 3 candles
    bars = mt5.copy_rates_from_pos(symbol, getattr(mt5, timeframe), 0, 3)

    if bars is None or len(bars) < 3:
        return "NONE", None, None

    close1 = bars[-1]['close']  # Current close
    close2 = bars[-2]['close']  # Previous close

    # Dummy crossover logic
    if close1 > close2:
        signal = "BUY"
        sl = close1 - 0.0015  # 15 pips SL
        tp = close1 + 0.0030  # 30 pips TP
    elif close1 < close2:
        signal = "SELL"
        sl = close1 + 0.0015
        tp = close1 - 0.0030
    else:
        signal = "NONE"
        sl = None
        tp = None

    return signal, sl, tp