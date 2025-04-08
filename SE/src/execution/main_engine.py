from signal_generator import check_signal
from user_prompt import ask_for_approval
from trade_executor import place_trade
from risk_manager import calculate_lot_size
from log_manager import log_trade_success, log_trade_failure, log_rejection
import time
from datetime import datetime

# Dummy placeholder - should be implemented with MT5 API
from utils import is_candle_closed


def run_engine(symbols, timeframes, risk_pct):
    while True:
        for symbol in symbols:
            for tf in timeframes:
                if is_candle_closed(symbol, tf):
                    signal, sl, tp = check_signal(symbol, tf)
                    if signal in ["BUY", "SELL"]:
                        approved = ask_for_approval(symbol, tf, signal, sl, tp)

                        if approved:
                            lot = calculate_lot_size(symbol, risk_pct, sl)
                            trade_result = place_trade(symbol, signal, lot, sl, tp)

                            if trade_result['success']:
                                log_trade_success(symbol, tf, signal, lot, sl, tp,
                                                  trade_result['price'], trade_result['order_id'])
                            else:
                                log_trade_failure(symbol, tf, signal, lot, sl, tp,
                                                  trade_result['error_code'], trade_result['comment'])
                        else:
                            log_rejection(symbol, tf, signal)
        time.sleep(5)
