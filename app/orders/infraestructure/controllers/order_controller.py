from typing import List 
from fastapi import HTTPException, status 

from ...application.use_cases.create_order_use_case import CreateOrderUseCase
from ...application.dto.create_order_dto import CreateOrderDTO
from ...application.dto.order_response_dto import OrderResponseDTO, OrderListResponseDTO, OrderCreatedResponseDTO

from ...domain.entities.enums import OrderStatus
from ....shared.exceptions import NotFoundException, BusinessException 
from ....shared.responses import SuccessResponse, ErrorResponse 

class OrderController:
    
    def __init__(self, create_order_use_case: CreateOrderUseCase):
        self.create_order_use_case : CreateOrderUseCase 
        
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
                        "subototal": item.subtotal
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
        



