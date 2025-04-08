import csv
from datetime import datetime

def log_trade_success(symbol, timeframe, direction, lot, sl, tp, entry_price, order_id):
    with open('trade_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            symbol,
            timeframe,
            direction,
            lot,
            sl,
            tp,
            entry_price,
            order_id,
            "SUCCESS"
        ])

def log_trade_failure(symbol, timeframe, direction, lot, sl, tp, error_code, comment):
    with open('trade_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            symbol,
            timeframe,
            direction,
            lot,
            sl,
            tp,
            "N/A",
            "N/A",
            f"FAILED | Error: {error_code} | Comment: {comment}"
        ])

def log_rejection(symbol, timeframe, direction):
    with open('trade_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            symbol,
            timeframe,
            direction,
            "REJECTED"
        ])
