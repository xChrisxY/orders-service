from typing import List, Optional
from pydantic import BaseModel, Field, validator

class CreateOrderItemDTO(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

    @validator('product_id')
    def validate_product_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Product ID cannot be empty')
        return v.strip()

    @validator('product_name')
    def validate_product_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Product name cannot be empty')
        return v.strip()


class CreateDeliveryAddressDTO(BaseModel):
    street: str = Field(min_length=1)
    city: str = Field(min_length=1)
    state: str = Field(min_length=1)
    postal_code: str = Field(min_length=1)
    country: str = Field(default="Mexico")
    additional_info: Optional[str] = None

    @validator('street', 'city', 'state', 'postal_code')
    def validate_required_fields(cls, v):
        if not v or not v.strip():
            raise ValueError('This field cannot be empty')
        return v.strip()


class CreateOrderDTO(BaseModel):
    user_id: str
    restaurant_id: str
    items: List[CreateOrderItemDTO] = Field(min_items=1)
    delivery_address: CreateDeliveryAddressDTO
    notes: Optional[str] = None
    delivery_fee: float = Field(default=0.0, ge=0)
    tax_rate: float = Field(default=0.16, ge=0, le=1)  # 16% IVA by default

    @validator('user_id', 'restaurant_id')
    def validate_ids(cls, v):
        if not v or not v.strip():
            raise ValueError('ID cannot be empty')
        return v.strip()

    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('Order must have at least one item')
        return v

    class Config:
        schema_extra = {
            "example": {
                "user_id": "6571234567890abcdef12345",
                "restaurant_id": "6571234567890abcdef67890",
                "items": [
                    {
                        "product_id": "6571234567890abcdef11111",
                        "product_name": "Pizza Margherita",
                        "quantity": 2,
                        "unit_price": 150.0
                    }
                ],
                "delivery_address": {
                    "street": "Av. Revolución 123",
                    "city": "Ciudad de México",
                    "state": "CDMX",
                    "postal_code": "06700",
                    "country": "Mexico",
                    "additional_info": "Apt 4B"
                },
                "notes": "Sin cebolla, por favor",
                "delivery_fee": 25.0,
                "tax_rate": 0.16
            }
        }