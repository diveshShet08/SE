import MetaTrader5 as mt5
from datetime import datetime

def is_candle_closed(symbol: str, timeframe: str) -> bool:
    rates = mt5.copy_rates_from_pos(symbol, getattr(mt5, timeframe), 0, 2)
    if rates is None or len(rates) < 2:
        return False

    current_time = datetime.utcnow().timestamp()
    last_candle_time = rates[-1]['time']

    # If the last candle's open time + duration < current time, candle is closed
    timeframe_seconds = tf_to_seconds(timeframe)
    return (last_candle_time + timeframe_seconds) < current_time

def tf_to_seconds(timeframe: str) -> int:
    mapping = {
        'M1': 60,
        'M5': 300,
        'M15': 900,
        'M30': 1800,
        'H1': 3600,
        'H4': 14400,
        'D1': 86400
    }
    return mapping.get(timeframe.upper(), 60)