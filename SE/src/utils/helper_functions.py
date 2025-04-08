import pandas as pd
import numpy as np
from datetime import datetime, timezone

def round_order_size(quantity, step_size):
    """Rounds order quantity to the nearest valid step size."""
    return round(quantity / step_size) * step_size

def round_price(price, tick_size):
    """Rounds price to the nearest valid tick size."""
    return round(price / tick_size) * tick_size

def calculate_percentage_change(series: pd.Series):
    """Calculates percentage change in a price series."""
    return series.pct_change()

def calculate_volatility(series: pd.Series, window=14):
    """Calculates rolling standard deviation as a measure of volatility."""
    return series.rolling(window).std()

def unix_to_datetime(timestamp):
    """Converts Unix timestamp to readable datetime."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def datetime_to_unix(date_str, format="%Y-%m-%d %H:%M:%S"):
    """Converts a datetime string to a Unix timestamp."""
    dt = datetime.strptime(date_str, format)
    return int(dt.replace(tzinfo=timezone.utc).timestamp())

