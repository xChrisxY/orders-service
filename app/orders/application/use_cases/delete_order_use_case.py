from ...domain.entities.order import Order 
from ...domain.repositories.order_repository import OrderRepository 
from ....shared.exceptions import BusinessException, NotFoundException 

class DeleteOrderUseCase:
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository 
        
    async def execute(self, order_id: str) -> bool:
        
        success = await self.order_repository.delete(order_id)
        
        if not success:
            raise NotFoundException(f"Order with id {order_id} not found")

        return success
            
        