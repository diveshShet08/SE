# --- user_prompt.py ---

def ask_for_approval(symbol: str, timeframe: str, signal: str, sl: float, tp: float) -> bool:
    print("\n[Signal Generated]")
    print(f"Symbol: {symbol}")
    print(f"Timeframe: {timeframe}")
    print(f"Signal: {signal}")
    print(f"SL: {sl:.5f}, TP: {tp:.5f}")
    user_input = input("Execute this trade? (y/n): ").strip().lower()
    return user_input == 'y'