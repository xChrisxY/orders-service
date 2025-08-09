from typing import Union
from .rabbitmq_publisher import RabbitMQPublisher
from ...application.events.order_created_event import OrderCreatedEvent

class EventPublisher:
    
    def __init__(self, rabbitmq_publisher: RabbitMQPublisher):
        self.rabbitmq_publisher = rabbitmq_publisher
        
    async def publish(self, event: Union[OrderCreatedEvent]):
        try: 
            event_dict = event.model_dump()
            routing_key = event.event_type.replace('.', '.')
            
            self.rabbitmq_publisher.publish_message(
                routing_key=routing_key,
                message=event_dict
            )
        except Exception as e:
            print(f"Failed to publish event {event.event_type}: {e}")
            raise