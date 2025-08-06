from datetime import datetime, timedelta, timezone
from typing import Optional

from ...domain.entities.order import Order
from ...domain.entities.enums import OrderStatus
from ...domain.entities.value_objects import DeliveryAddress, OrderItem

from ...domain.repositories.order_repository import OrderRepository

from ..dto.create_order_dto import CreateOrderDTO 
from ..dto.order_response_dto import OrderResponseDTO

from ....shared.exceptions import BusinessException


class CreateOrderUseCase:
    
    def __init__(self, order_repository: OrderRepository, event_publisher: Optional[object] = None):
        self.order_repository = order_repository
        self.event_publisher = event_publisher
        
    async def execute(self, order_dto: CreateOrderDTO) -> Order:
        
        try:
            
            order_items = []
            for item_dto in order_dto.items: 
                subtotal = item_dto.quantity * item_dto.unit_price
                order_item = OrderItem(
                    product_id=item_dto.product_id,
                    product_name=item_dto.product_name, 
                    quantity=item_dto.quantity, 
                    unit_price=item_dto.unit_price, 
                    subtotal=subtotal
                )
                
                order_items.append(order_item)
                
            delivery_address = DeliveryAddress(
                street=order_dto.delivery_address.street, 
                city=order_dto.delivery_address.city,
                state=order_dto.delivery_address.state, 
                postal_code=order_dto.delivery_address.postal_code,
                country=order_dto.delivery_address.country,
                additional_info=order_dto.delivery_address.additional_info
            )
            
            total_amount = sum(item.subtotal for item in order_items)
            tax_amount = total_amount * order_dto.tax_rate
            final_amount = total_amount + order_dto.delivery_fee + tax_amount
            
            order = Order(
                user_id=order_dto.user_id,
                restaurant_id=order_dto.restaurant_id,
                items=order_items,
                delivery_address=delivery_address,
                notes=order_dto.notes,
                delivery_fee=order_dto.delivery_fee,
                tax_amount=tax_amount,
                total_amount=total_amount,
                status=OrderStatus.PENDING,
                final_amount=final_amount,
                estimated_delivery_time=self._calculate_estimated_delivery_time(),
            )
            
            created_order = await self.order_repository.create(order)
            
            # Publish order created event for SAGA orchestration
            
            if self.event_publisher:
                pass 
            
            return created_order
         
        except Exception as e: 
            raise BusinessException(f"Failed to create order: {str(e)}")
        
    def _calculate_estimated_delivery_time(self) -> datetime:
        """Calculate estimated delivery time (30-45 minutes from now)"""
        import random
        delivery_minutes = random.randint(30, 45)
        return datetime.now(timezone.utc) + timedelta(minutes=delivery_minutes)