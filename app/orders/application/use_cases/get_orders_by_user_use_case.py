import math 
from typing import List, Dict, Any 
from ...domain.entities.order import Order 
from ...domain.repositories.order_repository import OrderRepository 

class GetOrdersByUserUseCase: 
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        
    async def execute(self, user_id: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        
        skip = (page - 1) * per_page 
        
        orders = await self.order_repository.get_by_user_id(user_id=user_id, limit=per_page, skip=skip)
        
        # implementar el total
        total = 0
        
        total_pages = math.ceil(total / per_page) if total > 0 else 1 
        
        return {
            "orders": orders, 
            "total": total, 
            "per_page" : per_page, 
            "total_pages": total_pages
        }