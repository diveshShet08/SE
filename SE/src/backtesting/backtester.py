import pandas as pd
import os
import numpy as np
import argparse
from datetime import datetime
from src.backtesting.performance_metrics import PerformanceMetrics
from src.backtesting.trade_execution import TradeExecution
from src.backtesting.trade_logging import TradeLogger
from src.strategies.strategy import Strategy

class Backtester:
    def __init__(self, strategy_name, currency_pair, timeframes, market_data, strategy_config):
        self.strategy = Strategy(strategy_name, market_data, strategy_config)
        print(type(self.strategy))
        print(np.shape(self.strategy))
        print(self.strategy[0])
        print("Done with Strategy()!")
        self.currency_pair = currency_pair
        self.timeframes = timeframes
        self.data = market_data
        self.execution = TradeExecution()
        print("Done with TradeExecution()!")
        self.logger = TradeLogger()
        print("Done with TradeLogger()!")
        # self.metrics = PerformanceMetrics()
        self.metrics = PerformanceMetrics(trades=pd.DataFrame(columns=['timestamp', 'symbol', 'entry_price', 'exit_price', 'quantity', 'side', 'profit_loss']))

        print("Done with PerformanceMetrics()!")
        self.results = []
        print("Done with generating results!")
        

    def run(self):
        i = 0
        while i < len(self.strategy):
            signal = self.strategy[i]
            idx, typee, entry_price, sl, tp = signal['row'], signal['type'], signal['price'], signal['sl'], signal['tp']

            if typee in ["BUY", "SELL"]:
                # Start scanning forward in price data to determine exit
                price_data = self.data.iloc[idx + 1:].reset_index(drop=True)

                hit_sl, hit_tp, exit_price, exit_idx = self.check_exit_condition(price_data, sl, tp, typee)

                trade = self.execution.execute_trade(idx, exit_idx, typee, entry_price, sl, tp, exit_price, hit_sl, hit_tp)
                self.logger.log_trade(trade)
                self.results.append(trade)

                # Move index forward to next trade signal after current trade exits
                i += 1  # Move to the next signal if "HOLD"

        self.save_results()
        return self.metrics.calculate(self.results)

    def check_exit_condition(self, price_data, sl, tp, trade_type):
        """
        Determines whether SL or TP is hit first.
        :param price_data: DataFrame starting from the trade entry index
        :param sl: Stop Loss price level
        :param tp: Take Profit price level
        :param trade_type: 'BUY' or 'SELL'
        :return: (hit_sl, hit_tp, exit_price, exit_idx)
        """
        for idx, row in price_data.iterrows():
            if trade_type == "BUY":
                if row["Low"] <= sl:  # Stop Loss hit first
                    return True, False, sl, idx
                if row["High"] >= tp:  # Take Profit hit first
                    return False, True, tp, idx
            elif trade_type == "SELL":
                if row["High"] >= sl:  # Stop Loss hit first
                    return True, False, sl, idx
                if row["Low"] <= tp:  # Take Profit hit first
                    return False, True, tp, idx

        # If neither SL nor TP is hit, exit at the last available close price
        return False, False, price_data.iloc[-1]["Close"], len(price_data) - 1

    def save_results(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        iteration = len(os.listdir(f"src/backtesting/{date_str}")) if os.path.exists(f"src/backtesting/{date_str}") else 0
        output_file = f"src/backtesting/{date_str}/{iteration}.csv"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        pd.DataFrame(self.results).to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the backtester with specified parameters.")
    parser.add_argument("--symbol", type=str, required=True, help="Currency pair (e.g., EURUSD)")
    parser.add_argument("--strategy", type=str, required=True, help="Strategy name (e.g., BollingerBands)")
    parser.add_argument("--timeframes", type=str, required=True, help="Comma-separated list of timeframes (e.g., 5min,15min)")
    parser.add_argument("--config", type=str, required=True, help="Comma-separated key:value pairs of strategy parameters")
    
    args = parser.parse_args()
    
    strategy_name = args.strategy
    currency_pair = args.symbol
    timeframes = args.timeframes.split(",")
    strategy_config = dict(item.split(":") for item in args.config.split(","))
    
    # Load historical market data
    # file_path = f"/home/niveus/Downloads/SE/base_v1/SE/src/data/historical/{currency_pair}.csv"
    #             # /home/niveus/Downloads/SE/base_v1/SE/src/data/historical/AUDCAD.csv
    file_path = os.path.join(os.getcwd(), "src", "data", "historical", f"{currency_pair}.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Historical data file not found: {file_path}")
    
    market_data = pd.read_csv(file_path)
    
    print("-----------------")
    print(strategy_name)
    print(strategy_config)
    print(currency_pair)
    print(timeframes)
    print("-----------------")
    
    # Convert numerical values in config to int/float
    for key, value in strategy_config.items():
        if value.replace('.', '', 1).isdigit():
            strategy_config[key] = float(value) if '.' in value else int(value)
    
    backtester = Backtester(strategy_name, currency_pair, timeframes, market_data, strategy_config)
    performance_report = backtester.run()
    print(performance_report)

# python3 backtesting/backtester.py --symbol "AUDCAD" --strategy "BollingerBands" --timeframes "5min,15min" --config "window:20,num_std:2"
# python3 -m src.backtesting.backtester --symbol "AUDCAD" --strategy "CombinedStrategyBB_RSI" --timeframes "5min,15min" --config "window:20,num_std:2"
