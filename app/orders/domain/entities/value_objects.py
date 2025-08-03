from typing import Optional
from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    product_id: str 
    product_name: str 
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    subtotal: float = Field(gt=0)
    
    def calculate_subtotal(self) -> float: 
        return self.quantity * self.unit_price 
    
class DeliveryAddress(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str = "Mexico"
    additional_info: Optional[str] = None 