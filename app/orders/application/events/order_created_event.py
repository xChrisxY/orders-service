from pydantic import BaseModel 
from ...domain.entities.order import OrderItem 
from typing import List 
from datetime import datetime

class OrderCreatedEvent(BaseModel):
    event_type: str = "order.created"
    order_id: str 
    user_id: str 
    restaurant_id: str 
    total_amount: float 
    items: List[OrderItem]
    created_at: datetime

    class Config: 
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    