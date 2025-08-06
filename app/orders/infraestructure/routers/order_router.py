from fastapi import APIRouter, Depends, status, Query
from typing import Optional 

from ..controllers.order_controller import OrderController 
from ...application.dto.create_order_dto import CreateOrderDTO 
from ...application.dto.order_response_dto import OrderResponseDTO, OrderCreatedResponseDTO, OrderListResponseDTO 

from ..dependencies import get_order_controller

from ...domain.entities.enums import OrderStatus 
from ....shared.responses import SuccessResponse 

router = APIRouter(prefix="/api/v1/orders", tags=["orders"]) 

@router.post(
    "/", 
    response_model=SuccessResponse[OrderCreatedResponseDTO], 
    status_code=status.HTTP_201_CREATED, 
    summary="Create a new order", 
    description="Create a new order with items and delivery address"
)
async def create_order(order_dto: CreateOrderDTO, controller: OrderController = Depends(get_order_controller)):
    return await controller.create_order(order_dto)

    
@router.get(
    "/{order_id}", 
    response_model=SuccessResponse[OrderResponseDTO], 
    status_code=status.HTTP_200_OK, 
    summary="Get order by ID", 
    description="Retrieve a specific order by its ID"
)
async def get_order(order_id: str, controller: OrderController = Depends(get_order_controller)):
    return await controller.get_order(order_id)

@router.get(
    "/user/{user_id}", 
    response_model=SuccessResponse[OrderListResponseDTO],
    status_code=status.HTTP_200_OK, 
    summary="Get orders by user", 
    description="Retrieve all orders for a specific user with pagination" 
)
async def get_orders_by_user(
    user_id: str, 
    page: int = Query(1, ge=1, description="Page number"), 
    per_page: int = Query(10, ge=1, le=100, description="Items per page"), 
    controller: OrderController = Depends(get_order_controller)
    
):
    # Get orders with filters (for admin/restaurant use)
    return await controller.get_orders_by_user("", page, per_page)

@router.put(
    "/{order_id}",
    response_model=SuccessResponse[OrderResponseDTO],
    status_code=status.HTTP_200_OK, 
    summary="Update order status",
    description="Update the status of a specific order"
)
async def update_order_status(
    order_id: str, 
    new_status: OrderStatus = Query(..., description="New status for the order"),
    controller: OrderController = Depends(get_order_controller)
):
    return await controller.update_order_status(order_id, new_status) 

@router.delete(
    "/{order_id}", 
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK, 
    summary="Delete order",
    description="Delete a specific order"
)
async def delete_order(order_id: str, controller: OrderController = Depends(get_order_controller)):
    return await controller.delete_order(order_id)