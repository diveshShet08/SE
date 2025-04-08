class RiskEngine:
    def __init__(self, max_risk_per_trade=0.02, account_balance=10000):
        """
        max_risk_per_trade: Max % risk per trade (e.g., 2%)
        account_balance: Total capital
        """
        self.max_risk_per_trade = max_risk_per_trade
        self.account_balance = account_balance

    def validate_trade(self, symbol: str, entry_price: float, stop_loss: float, position_size: int):
        """Check if trade follows risk rules."""
        risk_per_trade = abs(entry_price - stop_loss) * position_size
        max_allowed_risk = self.account_balance * self.max_risk_per_trade
        return risk_per_trade <= max_allowed_risk

    def dynamic_position_sizing(self, entry_price: float, stop_loss: float):
        """Calculate position size based on risk per trade."""
        risk_per_share = abs(entry_price - stop_loss)
        max_risk = self.account_balance * self.max_risk_per_trade
        return int(max_risk / risk_per_share) if risk_per_share > 0 else 0

