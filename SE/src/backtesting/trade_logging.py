import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class TradeLogger:
    def __init__(self, log_file="trades.csv", log_level=logging.INFO):
        self.log_file = log_file
        self.logger = logging.getLogger("TradeLogger")
        self.logger.setLevel(log_level)
        
        handler = logging.FileHandler("trade_execution.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        
        self.trades = []  # Stores trade data before saving to file

    def log_trade(self, trade):
        """Logs a trade and appends it to the trade list."""
        self.trades.append(trade)
        self.logger.info(f"Trade Executed: {trade}")
    
    def save_trades(self):
        """Saves all trades to a CSV file."""
        df = pd.DataFrame(self.trades)
        df.to_csv(self.log_file, index=False)
        self.logger.info("Trade log saved to file.")

class TradeVisualizer:
    def __init__(self, trade_log_file="trades.csv"):
        self.trade_log_file = trade_log_file
    
    def load_trades(self):
        """Loads the trade log from CSV."""
        try:
            return pd.read_csv(self.trade_log_file)
        except FileNotFoundError:
            print("Trade log file not found.")
            return None
    
    def plot_equity_curve(self):
        """Plots the equity curve based on cumulative returns."""
        trades = self.load_trades()
        if trades is None:
            return
        
        trades["cumulative_pnl"] = trades["pnl"].cumsum()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=trades, x=trades.index, y="cumulative_pnl", label="Equity Curve")
        plt.xlabel("Trades")
        plt.ylabel("Cumulative PnL")
        plt.title("Equity Curve")
        plt.grid()
        plt.show()

    def plot_drawdown(self):
        """Plots drawdown from peak equity."""
        trades = self.load_trades()
        if trades is None:
            return
        
        trades["cumulative_pnl"] = trades["pnl"].cumsum()
        trades["peak"] = trades["cumulative_pnl"].cummax()
        trades["drawdown"] = trades["peak"] - trades["cumulative_pnl"]
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=trades, x=trades.index, y="drawdown", label="Drawdown", color="red")
        plt.xlabel("Trades")
        plt.ylabel("Drawdown Amount")
        plt.title("Drawdown Analysis")
        plt.grid()
        plt.show()

# Example Usage
# logger = TradeLogger()
# logger.log_trade({"symbol": "EUR/USD", "side": "buy", "size": 1.0, "pnl": 50})
# logger.save_trades()

# visualizer = TradeVisualizer()
# visualizer.plot_equity_curve()
# visualizer.plot_drawdown()
