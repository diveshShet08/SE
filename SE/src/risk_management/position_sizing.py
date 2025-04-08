class PositionSizing:
    def __init__(self, risk_per_trade=0.01, account_balance=10000):
        self.risk_per_trade = risk_per_trade
        self.account_balance = account_balance

    def calculate_size(self, entry_price, stop_loss_price):
        """Calculates optimal position size based on risk tolerance."""
        risk_amount = self.account_balance * self.risk_per_trade
        risk_per_share = abs(entry_price - stop_loss_price)
        position_size = risk_amount / risk_per_share
        return max(1, int(position_size))  # Ensure at least 1 share/unit

