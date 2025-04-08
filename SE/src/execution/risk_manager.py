import MetaTrader5 as mt5

def get_account_balance():
    account_info = mt5.account_info()
    return account_info.balance if account_info is not None else 0

def get_tick_size(symbol: str) -> float:
    info = mt5.symbol_info(symbol)
    return info.trade_tick_size if info is not None else 0.0001

def calculate_lot_size(symbol: str, risk_pct: float, sl_price: float) -> float:
    balance = get_account_balance()
    risk_amount = balance * (risk_pct / 100)

    # Get latest price for pip distance
    tick = mt5.symbol_info_tick(symbol)
    current_price = tick.ask if tick is not None else 1.0

    sl_distance = abs(current_price - sl_price)
    if sl_distance == 0:
        return 0.01  # minimum lot size fallback

    tick_value = get_tick_size(symbol)
    lot_size = risk_amount / (sl_distance / tick_value)

    # Round to 2 decimal places and respect broker min lot
    return max(round(lot_size, 2), 0.01)