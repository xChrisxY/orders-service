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
        
    
        
