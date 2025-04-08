import importlib
import inspect
import os
import pandas as pd

def list_available_strategies():
    """Dynamically lists available strategies in the 'src/strategies/' directory."""
    strategy_path = "/home/niveus/Downloads/SE/base_v1/SE/src/strategies"
    return [f[:-3] for f in os.listdir(strategy_path) if f.endswith(".py") and f != "__init__.py"]

def get_strategy(strategy_name, config):
    """Dynamically imports and initializes the specified strategy class with user-provided parameters."""
    try:
        module = importlib.import_module(f"src.strategies.{strategy_name}")
        StrategyClass = getattr(module, strategy_name)
    except (ModuleNotFoundError, AttributeError):
        print(f"[ERROR] Strategy '{strategy_name}' not found. Available strategies:")
        print(" - " + ", ".join(list_available_strategies()))
        exit(1)
    
    required_params = list(inspect.signature(StrategyClass.__init__).parameters.keys())[1:]  # Exclude 'self'
    final_config = {}

    for param in required_params:
        if param in config:
            try:
                final_config[param] = float(config[param]) if "." in config[param] else int(config[param])
            except ValueError:
                final_config[param] = config[param]  # Keep as string if conversion fails
        else:
            final_config[param] = input(f"Enter value for {param}: ")

    return StrategyClass(**final_config)

def Strategy(strategy_name: str, market_data: pd.DataFrame, config: dict):
    """Runs the specified strategy on given market data."""
    strategy_instance = get_strategy(strategy_name, config)
    print("Straegy config input successful!")
    signals = strategy_instance.generate_signals(market_data)
    return signals
