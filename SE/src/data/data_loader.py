import pandas as pd
import requests

class DataLoader:
    def __init__(self, source: str):
        """
        source: Can be 'csv', 'api', or 'database'
        """
        self.source = source

    def load_historical_data(self, symbol: str, start_date: str, end_date: str, file_path=None):
        """Load historical data from CSV or API."""
        if self.source == 'csv' and file_path:
            data = pd.read_csv(file_path, parse_dates=['date'])
            return data[(data['date'] >= start_date) & (data['date'] <= end_date)]

        elif self.source == 'api':
            response = requests.get(f"https://api.example.com/marketdata/{symbol}?start={start_date}&end={end_date}")
            return pd.DataFrame(response.json())

    def get_live_data(self, symbol: str):
        """Fetch real-time market data."""
        response = requests.get(f"https://api.example.com/livemarket/{symbol}")
        return response.json()  # Returns latest price, volume, etc.

