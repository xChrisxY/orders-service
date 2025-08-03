from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from ...domain.entities.order import OrderStatus

class OrderItemResponseDTO(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float


class DeliveryAddressResponseDTO(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    additional_info: Optional[str] = None


class OrderResponseDTO(BaseModel):
    id: str
    user_id: str
    restaurant_id: str
    items: List[OrderItemResponseDTO]
    delivery_address: DeliveryAddressResponseDTO
    status: OrderStatus
    total_amount: float
    delivery_fee: float
    tax_amount: float
    final_amount: float
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    estimated_delivery_time: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class OrderListResponseDTO(BaseModel):
    orders: List[OrderResponseDTO]
    total: int
    page: int
    per_page: int
    total_pages: int

    class Config:
        from_attributes = True


class OrderCreatedResponseDTO(BaseModel):
    order: OrderResponseDTO
    message: str = "Order created successfully"

    class Config:
        from_attributes = True