from typing import List 
from fastapi import HTTPException, status 

from ...application.use_cases.create_order_use_case import CreateOrderUseCase
from ...application.use_cases.get_order_use_case import GetOrderUseCase
from ...application.use_cases.get_orders_by_user_use_case import GetOrdersByUserUseCase
from ...application.use_cases.update_order_status_use_case import UpdateOrderStatusUseCase
from ...application.use_cases.delete_order_use_case import DeleteOrderUseCase

from ...application.dto.create_order_dto import CreateOrderDTO
from ...application.dto.order_response_dto import OrderResponseDTO, OrderListResponseDTO, OrderCreatedResponseDTO

from ...domain.entities.enums import OrderStatus
from ....shared.exceptions import NotFoundException, BusinessException 
from ....shared.responses import SuccessResponse, ErrorResponse 

class OrderController:
    
    def __init__(self, 
        create_order_use_case: CreateOrderUseCase,
        get_order_use_case: GetOrderUseCase,
        get_orders_by_user_use_case: GetOrdersByUserUseCase,
        update_order_status_use_case: UpdateOrderStatusUseCase, 
        delete_order_use_case: DeleteOrderUseCase
    ):
        self.create_order_use_case = create_order_use_case
        self.get_order_use_case = get_order_use_case
        self.get_orders_by_user_use_case = get_orders_by_user_use_case
        self.update_order_status_use_case = update_order_status_use_case
        self.delete_order_use_case = delete_order_use_case
        
    async def create_order(self, order_dto: CreateOrderDTO) -> SuccessResponse:
        
        try: 
            
            order = await self.create_order_use_case.execute(order_dto)
            
            order_response = OrderResponseDTO(
                id=order.id, 
                user_id=order.user_id, 
                restaurant_id=order.restaurant_id, 
                items=[
                    {
                        "product_id": item.product_id, 
                        "product_name": item.product_name, 
                        "quantity": item.quantity, 
                        "unit_price": item.unit_price, 
                        "subtotal": item.subtotal
                    }
                    for item in order.items
                ],
                delivery_address={
                    "street": order.delivery_address.street,
                    "city": order.delivery_address.city,
                    "state": order.delivery_address.state,
                    "postal_code": order.delivery_address.postal_code,
                    "country": order.delivery_address.country,
                    "additional_info": order.delivery_address.additional_info 
                },
                status=order.status, 
                total_amount=order.total_amount,
                delivery_fee=order.delivery_fee,
                tax_amount=order.tax_amount,
                final_amount=order.final_amount,
                notes=order.notes,
                created_at=order.created_at,
                updated_at=order.updated_at,
                estimated_delivery_time=order.estimated_delivery_time,
                delivered_at=order.delivered_at
            )

            response_data = OrderCreatedResponseDTO(order=order_response)
            
            return SuccessResponse(
                data=response_data, 
                message="Order created successfully", 
                status_code=status.HTTP_201_CREATED
            )
            
        except BusinessException as e: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=str(e)
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error: {str(e)}"
            )
    
    async def get_order(self, order_id: str) -> SuccessResponse:
        try:
            order = await self.get_order_use_case.execute(order_id)
            
            order_response = OrderResponseDTO(
                id=order.id, 
                user_id=order.user_id, 
                restaurant_id=order.restaurant_id, 
                items=[
                    {
                        "product_id": item.product_id, 
                        "product_name": item.product_name, 
                        "quantity": item.quantity, 
                        "unit_price": item.unit_price, 
                        "subtotal": item.subtotal
                    }
                    for item in order.items
                ],
                delivery_address={
                    "street": order.delivery_address.street,
                    "city": order.delivery_address.city,
                    "state": order.delivery_address.state,
                    "postal_code": order.delivery_address.postal_code,
                    "country": order.delivery_address.country,
                    "additional_info": order.delivery_address.additional_info 
                },
                status=order.status, 
                total_amount=order.total_amount,
                delivery_fee=order.delivery_fee,
                tax_amount=order.tax_amount,
                final_amount=order.final_amount,
                notes=order.notes,
                created_at=order.created_at,
                updated_at=order.updated_at,
                estimated_delivery_time=order.estimated_delivery_time,
                delivered_at=order.delivered_at
            )
            
            return SuccessResponse(
                data=order_response, 
                message="Order retrieved successfully", 
                status_code=status.HTTP_200_OK
            )
            
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error: {str(e)}"
            )
    
    async def get_orders_by_user(self, user_id: str, limit: int = 10, skip: int = 0) -> SuccessResponse:
        try:
            orders = await self.get_orders_by_user_use_case.execute(user_id, limit, skip)
            
            orders_response = [
                OrderResponseDTO(
                    id=order.id, 
                    user_id=order.user_id, 
                    restaurant_id=order.restaurant_id, 
                    items=[
                        {
                            "product_id": item.product_id, 
                            "product_name": item.product_name, 
                            "quantity": item.quantity, 
                            "unit_price": item.unit_price, 
                            "subtotal": item.subtotal
                        }
                        for item in order.items
                    ],
                    delivery_address={
                        "street": order.delivery_address.street,
                        "city": order.delivery_address.city,
                        "state": order.delivery_address.state,
                        "postal_code": order.delivery_address.postal_code,
                        "country": order.delivery_address.country,
                        "additional_info": order.delivery_address.additional_info 
                    },
                    status=order.status, 
                    total_amount=order.total_amount,
                    delivery_fee=order.delivery_fee,
                    tax_amount=order.tax_amount,
                    final_amount=order.final_amount,
                    notes=order.notes,
                    created_at=order.created_at,
                    updated_at=order.updated_at,
                    estimated_delivery_time=order.estimated_delivery_time,
                    delivered_at=order.delivered_at
                )
                for order in orders
            ]
            
            response_data = OrderListResponseDTO(orders=orders_response)
            
            return SuccessResponse(
                data=response_data, 
                message="Orders retrieved successfully", 
                status_code=status.HTTP_200_OK
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error: {str(e)}"
            )
    
    async def update_order_status(self, order_id: str, new_status: OrderStatus) -> SuccessResponse: 
        
        try: 
            
            order = await self.update_order_status_use_case.execute(order_id, new_status)

            order_response = OrderResponseDTO(
                id=order.id, 
                user_id=order.user_id, 
                restaurant_id=order.restaurant_id, 
                items=[
                    {
                        "product_id": item.product_id, 
                        "product_name": item.product_name, 
                        "quantity": item.quantity, 
                        "unit_price": item.unit_price, 
                        "subtotal": item.subtotal
                    }
                    for item in order.items
                ],
                delivery_address={
                    "street": order.delivery_address.street,
                    "city": order.delivery_address.city,
                    "state": order.delivery_address.state,
                    "postal_code": order.delivery_address.postal_code,
                    "country": order.delivery_address.country,
                    "additional_info": order.delivery_address.additional_info 
                },
                status=order.status, 
                total_amount=order.total_amount,
                delivery_fee=order.delivery_fee,
                tax_amount=order.tax_amount,
                final_amount=order.final_amount,
                notes=order.notes,
                created_at=order.created_at,
                updated_at=order.updated_at,
                estimated_delivery_time=order.estimated_delivery_time,
                delivered_at=order.delivered_at
            )

            return SuccessResponse(
                data=order_response, 
                message="Order retrieved successfully", 
                status_code=status.HTTP_200_OK
            )

        except NotFoundException as e: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=str(e)
            )

        except BusinessException as e: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=str(e)
            )
        
        except Exception as e: 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Interal Server Error: {str(e)}"
            )

    async def delete_order(self, order_id: str) -> SuccessResponse:
        
        try: 
            
            await self.delete_order_use_case.execute(order_id)

            return SuccessResponse(
                data={"deleted_order_id": order_id},
                message="Order deleted successfully",
                status_code=status.HTTP_200_OK
            )

        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=str(e)
            )
        except Exception as e: 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Internal Server Error: {str(e)}"
            )
            
            
        



