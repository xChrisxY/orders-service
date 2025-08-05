from ...domain.entities.order import Order 
from ...domain.repositories.order_repository import OrderRepository 
from ....shared.exceptions import NotFoundException

class GetOrderUseCase:
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository 
        
    async def execute(self, order_id: str) -> Order: 
        order = await self.order_repository.get_by_id(order_id)
        
        if not order: 
            raise NotFoundException(f"Order with id {order_id} not found")
        
        return order
        