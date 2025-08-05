from fastapi import APIRouter, Depends, status
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