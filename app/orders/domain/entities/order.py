from datetime import datetime, timezone
from typing import List, Optional 
from pydantic import BaseModel, Field 
from bson import ObjectId 

from .enums import OrderStatus 
from .value_objects import OrderItem, DeliveryAddress 

class Order(BaseModel): 
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str 
    restaurant_id: str 
    items: List[OrderItem]
    delivery_address: DeliveryAddress
    status: OrderStatus = OrderStatus.PENDING
    total_amount: float = Field(gt=0)
    delivery_fee: float = Field(default=0.0, ge=0)
    tax_amount: float = Field(default=0.0, ge=0)
    final_amount: float = Field(gt=0)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    estimated_delivery_time: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True 
        json_encoders = {
            ObjectId: str, 
            datetime: lambda v: v.isoformat()
        }
        
    def calculate_total(self) -> float: 
        items_total = sum(item.subtotal for item in self.items)
        return items_total 
    
    def calculate_final_amount(self) -> float: 
        return self.total_amount + self.delivery_fee + self.tax_amount
    
    def update_status(self, new_status: OrderStatus) -> None: 
        self.status = new_status 
        self.updated_at = datetime.now(timezone.utc)
        
        if new_status == OrderStatus.DELIVERED: 
            self.delivered_at = datetime.now(timezone.utc)
            
    def is_cancellable(self) -> bool: 
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    def is_modifiable(self) -> bool: 
        return self.status == OrderStatus.PENDING