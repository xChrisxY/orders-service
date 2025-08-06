from functools import lru_cache
from ...config.database import get_database
from ..domain.repositories.order_repository import OrderRepository
from ..infraestructure.repositories.mongodb_order_repository import MongoDBOrderRepository
from ..application.use_cases.create_order_use_case import CreateOrderUseCase
from ..application.use_cases.get_order_use_case import GetOrderUseCase
from ..application.use_cases.get_orders_by_user_use_case import GetOrdersByUserUseCase
from ..application.use_cases.update_order_status_use_case import UpdateOrderStatusUseCase
from ..application.use_cases.delete_order_use_case import DeleteOrderUseCase
from ..infraestructure.controllers.order_controller import OrderController

# Repository dependencies
@lru_cache()
def get_order_repository() -> OrderRepository:
    """Get order repository instance"""
    database = get_database()
    return MongoDBOrderRepository(database)


# Use case dependencies
@lru_cache()
def get_create_order_use_case() -> CreateOrderUseCase:
    """Get create order use case instance"""
    order_repository = get_order_repository()
    return CreateOrderUseCase(order_repository)


@lru_cache()
def get_get_order_use_case() -> GetOrderUseCase:
    """Get order use case instance"""
    order_repository = get_order_repository()
    return GetOrderUseCase(order_repository)


@lru_cache()
def get_get_orders_by_user_use_case() -> GetOrdersByUserUseCase:
    """Get orders by user use case instance"""
    order_repository = get_order_repository()
    return GetOrdersByUserUseCase(order_repository)

@lru_cache()
def get_update_order_status_use_case() -> UpdateOrderStatusUseCase:
    order_repository = get_order_repository()
    return UpdateOrderStatusUseCase(order_repository)

@lru_cache()
def get_delete_order_use_case() -> DeleteOrderUseCase:
    order_repository = get_order_repository() 
    return DeleteOrderUseCase(order_repository)

# Controller dependencies
@lru_cache()
def get_order_controller() -> OrderController:
    """Get order controller instance"""
    create_order_use_case = get_create_order_use_case()
    get_order_use_case = get_get_order_use_case()
    get_orders_by_user_use_case = get_get_orders_by_user_use_case()
    update_order_use_case = get_update_order_status_use_case()
    delete_order_use_case = get_delete_order_use_case()
    
    return OrderController(
        create_order_use_case=create_order_use_case,
        get_order_use_case=get_order_use_case,
        get_orders_by_user_use_case=get_orders_by_user_use_case,
        update_order_status_use_case=update_order_use_case, 
        delete_order_use_case=delete_order_use_case
    )