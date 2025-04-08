class StopLoss:
    def __init__(self, stop_loss_percent=0.02):
        self.stop_loss_percent = stop_loss_percent

    def calculate_stop_loss(self, entry_price):
        """Calculates stop-loss price based on % risk."""
        stop_loss_price = entry_price * (1 - self.stop_loss_percent)
        return round(stop_loss_price, 2)

