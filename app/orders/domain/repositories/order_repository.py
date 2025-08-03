from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.order import Order, OrderStatus

class OrderRepository(ABC):
    
    @abstractmethod
    async def create(self, order: Order) -> Order: 
        pass    

    @abstractmethod 
    async def get_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod 
    async def get_by_user_id(self, user_id: str, limit: int = 10, skip: int = 0) -> List[Order]: 
        pass 
    
    @abstractmethod
    async def update_status(self, order_id: str, status: OrderStatus) -> bool:
        pass 
    
    @abstractmethod
    async def update(self, order: Order) -> Order: 
        pass

    @abstractmethod
    async def delete(self, order_id: str) -> bool: 
        pass 
    
    @abstractmethod 
    async def get_by_restaurant_id(self, restaurant_id: str, limit: int = 10, skip: int = 0) -> List[Order]:
        pass 
    
    @abstractmethod 
    async def get_by_status(self, status: OrderStatus, limit: int = 10, skip: int = 0) -> List[List]:
        pass