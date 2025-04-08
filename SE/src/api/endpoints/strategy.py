from fastapi import APIRouter
from strategies.mean_reversion import MeanReversionStrategy

router = APIRouter()
strategy = MeanReversionStrategy()  # Initialize strategy

@router.post("/start")
def start_strategy():
    """Starts the trading strategy."""
    strategy.start()
    return {"message": "Strategy started"}

@router.post("/stop")
def stop_strategy():
    """Stops the trading strategy."""
    strategy.stop()
    return {"message": "Strategy stopped"}

@router.get("/status")
def strategy_status():
    """Returns strategy status (running/stopped)."""
    return {"status": strategy.status()}

