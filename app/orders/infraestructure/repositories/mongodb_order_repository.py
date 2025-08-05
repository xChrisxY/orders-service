from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...domain.entities.order import Order 
from ...domain.entities.enums import OrderStatus
from ...domain.repositories.order_repository import OrderRepository
from ....shared.exceptions import NotFoundException

class MongoDBOrderRepository(OrderRepository):
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database 
        self.collection = database.orders 
        
    async def create(self, order: Order) -> Order:
        
        order_dict = order.model_dump(by_alias=True, exclude={"id"})
        
        result = await self.collection.insert_one(order_dict)
        
        created_order = await self.collection.find_one({"_id": result.inserted_id})
        
        return Order(**created_order)
    
    async def get_by_id(self, order_id: str) -> Optional[Order]:
        
        try: 
            object_id = ObjectId(order_id)
            order_doc = await self.collection.find_one({"_id": object_id})
            
            if order_doc:
                return Order(**order_doc)
            return None 
        except Exception:
            return None

    async def get_by_user_id(self, user_id, limit = 10, skip = 0):
        return await super().get_by_user_id(user_id, limit, skip)  
    
    async def update_status(self, order_id, status):
        return await super().update_status(order_id, status)

    async def update(self, order):
        return await super().update(order)

    async def delete(self, order_id):
        return await super().delete(order_id)

    async def get_by_restaurant_id(self, restaurant_id, limit = 10, skip = 0):
        return await super().get_by_restaurant_id(restaurant_id, limit, skip)

    async def get_by_status(self, status, limit = 10, skip = 0):
        return await super().get_by_status(status, limit, skip)
