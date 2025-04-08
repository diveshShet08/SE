import pandas as pd

class TradeExecution:
    def __init__(self, initial_balance=10000, risk_per_trade=0.01, leverage=10):
        self.balance = initial_balance
        self.equity = initial_balance
        self.risk_per_trade = risk_per_trade
        self.leverage = leverage
        self.positions = []
        self.trade_log = []
    
    def execute_trade(self, entry_idx, exit_idx, trade_type, entry_price, sl, tp, exit_price, hit_sl, hit_tp):
        """
        Executes a trade and returns a dictionary with trade details.

        :param entry_idx: Index where trade was entered
        :param exit_idx: Index where trade exited
        :param trade_type: 'BUY' or 'SELL'
        :param entry_price: Price at which trade was entered
        :param sl: Stop Loss level
        :param tp: Take Profit level
        :param exit_price: Price at which trade was closed
        :param hit_sl: Boolean, True if SL was hit
        :param hit_tp: Boolean, True if TP was hit
        :return: Trade dictionary
        """
        trade = {
            'timestamp': entry_idx,  # Add timestamp here
            'entry_idx': entry_idx,
            'exit_idx': exit_idx,
            'type': trade_type,
            'entry_price': entry_price,
            'stop_loss': sl,
            'take_profit': tp,
            'exit_price': exit_price,
            'hit_sl': hit_sl,
            'hit_tp': hit_tp,
            'profit_loss': (exit_price - entry_price) if trade_type == "BUY" else (entry_price - exit_price)
        }
        return trade
        
    def calculate_position_size(self, stop_loss_pips, pip_value=10):
        """
        Calculate position size based on risk per trade and stop loss distance.
        """
        risk_amount = self.balance * self.risk_per_trade
        position_size = (risk_amount / (stop_loss_pips * pip_value)) * self.leverage
        return round(position_size, 2)

    def open_trade(self, symbol, direction, entry_price, stop_loss, take_profit, volume):
        """
        Execute a trade and log it.
        """
        trade = {
            "symbol": symbol,
            "direction": direction,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "volume": volume,
            "status": "open"
        }
        self.positions.append(trade)
        return trade

    def close_trade(self, trade, exit_price):
        """
        Close a trade and update balance.
        """
        profit_loss = (exit_price - trade["entry_price"]) * trade["volume"] if trade["direction"] == "buy" else (trade["entry_price"] - exit_price) * trade["volume"]
        self.balance += profit_loss
        trade["exit_price"] = exit_price
        trade["profit_loss"] = profit_loss
        trade["status"] = "closed"
        self.positions.remove(trade)
        self.trade_log.append(trade)
        return trade

    def enforce_risk_limits(self, max_drawdown=0.2):
        """
        Check if drawdown exceeds risk limits.
        """
        if self.balance < (1 - max_drawdown) * self.equity:
            print("Risk limit hit! Stopping trading.")
            return False
        return True

    def get_trade_log(self):
        """
        Return trade history as DataFrame.
        """
        return pd.DataFrame(self.trade_log)

# Example usage:
# trade_exec = TradeExecution()
# position_size = trade_exec.calculate_position_size(10)
# trade = trade_exec.open_trade("EUR/USD", "buy", 1.1000, 1.0950, 1.1100, position_size)
# closed_trade = trade_exec.close_trade(trade, 1.1050)
# print(trade_exec.get_trade_log())
