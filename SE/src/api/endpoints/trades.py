from fastapi import APIRouter
from execution.broker_api import BrokerAPI

router = APIRouter()
broker = BrokerAPI()  # Initialize broker connection

@router.post("/place_order")
def place_order(symbol: str, qty: int, order_type: str = "market"):
    """Places a new order via broker API."""
    order_id = broker.place_order(symbol, qty, order_type)
    return {"message": "Order placed", "order_id": order_id}

@router.get("/order_status/{order_id}")
def order_status(order_id: str):
    """Fetch order status."""
    status = broker.get_order_status(order_id)
    return {"order_id": order_id, "status": status}

@router.post("/cancel_order/{order_id}")
def cancel_order(order_id: str):
    """Cancel an active order."""
    result = broker.cancel_order(order_id)
    return {"order_id": order_id, "message": result}

