from ...domain.entities.order import Order 
from ...domain.entities.enums import OrderStatus
from ...domain.repositories.order_repository import OrderRepository 
from ....shared.exceptions import BusinessException , NotFoundException

class UpdateOrderStatusUseCase: 
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        
    async def execute(self, order_id, new_status: OrderStatus) -> Order: 

        order = await self.order_repository.get_by_id(order_id)

        if not order:
            raise NotFoundException(f"Order with id {order_id} not found")
        
        order.update_status(new_status)

        updated_order = await self.order_repository.update(order)

        return updated_order
    