from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from src.strategies.BB1 import BollingerBandsStrategy  # ✅ Correct

# Initialize FastAPI app
app = FastAPI(title="The API", version="1.0")

# Sample Market Data (Normally, this would come from a live API or database)
market_data = pd.DataFrame({
    "date": pd.date_range(start="2024-03-01", periods=100, freq="D"),
    "close": [100 + i*0.5 for i in range(100)]  # Simulated price increase
})

# Request Model for Strategy Parameters
class BollingerBandsRequest(BaseModel):
    window: int = 20       # Moving Average window size
    std_factor: float = 2  # Multiplier for standard deviation

# Root Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Algo Trading API!"}

# Run Bollinger Bands Strategy
@app.post("/strategy/bollinger_bands")
def run_bollinger_bands(request: BollingerBandsRequest):
    try:
        # Initialize strategy
        strategy = BollingerBandsStrategy(window=request.window, std_factor=request.std_factor)
        strategy.load_data(market_data)
        
        # Generate signals
        signals = strategy.generate_signals()
        
        return signals.tail(10).to_dict(orient="records")  # Return last 10 rows for preview

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run API Server (Use "uvicorn main:app --reload" to start)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

