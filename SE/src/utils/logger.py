import logging

def setup_logger(log_file="algo_trading.log"):
    """Configures logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("algo_trading")

logger = setup_logger()
logger.info("Logger initialized.")

