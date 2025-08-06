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
        
        # Convert ObjectId to string for Pydantic model
        if created_order and "_id" in created_order:
            created_order["_id"] = str(created_order["_id"])
        
        return Order(**created_order)
    
    async def get_by_id(self, order_id: str) -> Optional[Order]:
        
        try: 
            object_id = ObjectId(order_id)
            order_doc = await self.collection.find_one({"_id": object_id})
            
            if order_doc:
                # Convert ObjectId to string for Pydantic model
                order_doc["_id"] = str(order_doc["_id"])
                return Order(**order_doc)
            return None 
        except Exception:
            return None

    async def get_by_user_id(self, user_id, limit = 10, skip = 0):
        return await super().get_by_user_id(user_id, limit, skip)  
    
    async def update_status(self, order_id: str, status: OrderStatus) -> bool:

        try: 
            
            object_id = ObjectId(order_id)
            order = await self.collection.find_one({"_id": object_id})

            if not order:
                return False

            from datetime import datetime, timezone
            update_data = {
                "status": status, 
                "updated_at": datetime.now(timezone.utc)
            }

            if status == OrderStatus.DELIVERED:
                update_data["delivered_at"] = datetime.now(timezone.utc)

            result = await self.collection.update_one(
                {"_id": object_id}, 
                {"$set": update_data}
            )

            return result.modified_count > 0
            
        except Exception: 
            return False 

    async def update(self, order: Order) -> Order:

        try: 
            object_id = ObjectId(order.id)
            order_dict = order.model_dump(by_alias=True, exclude={"id"})
            
            result = await self.collection.update_one(
                {"_id": object_id}, 
                {"$set": order_dict}
            )
            
            if result.modified_count == 0:
                raise NotFoundException(f"Order with id {order.id} not found")
            
            updated_order = await self.collection.find_one({"_id": object_id})
            return Order(**updated_order)
            
        except Exception as e: 
            raise NotFoundException(f"Order with id {order.id} not found")


    async def delete(self, order_id):

        try:
            object_id = ObjectId(order_id)
            
            result = await self.collection.delete_one({
                "_id" : object_id 
            })

            return result.deleted_count > 0
        
        except Exception as e:
            raise NotFoundException(f"Order with id {order_id} not found")

    async def get_by_restaurant_id(self, restaurant_id, limit = 10, skip = 0):
        return await super().get_by_restaurant_id(restaurant_id, limit, skip)

    async def get_by_status(self, status, limit = 10, skip = 0):
        return await super().get_by_status(status, limit, skip)
