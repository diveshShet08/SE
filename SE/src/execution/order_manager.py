import logging
from execution.broker_api import BrokerAPI

class OrderManager:
    def __init__(self):
        self.broker = BrokerAPI()

    def execute_trade(self, symbol, qty, order_type="market"):
        """Places an order and logs execution details."""
        order_id = self.broker.place_order(symbol, qty, order_type)
        logging.info(f"Executed trade: {symbol} | Qty: {qty} | Order Type: {order_type} | Order ID: {order_id}")
        return order_id

