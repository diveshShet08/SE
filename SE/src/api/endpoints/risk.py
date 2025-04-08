from fastapi import APIRouter
from risk_management.risk_engine import RiskEngine

router = APIRouter()
risk_engine = RiskEngine()

@router.get("/validate_trade")
def validate_trade(symbol: str, qty: int):
    """Validates if a trade is within risk limits."""
    is_valid = risk_engine.validate(symbol, qty)
    return {"symbol": symbol, "valid": is_valid}

