import json 
import pika 
from typing import Dict, Any 
from ....config.settings import settings

class RabbitMQPublisher:
    
    def __init__(self):
        self.connection = None 
        self.channel = None 
        self._connect()
        
    def _connect(self):
        
        try: 
            
            credentials = pika.PlainCredentials(
                settings.rabbitmq_username, 
                settings.rabbitmq_password
            )
            
            parameters = pika.ConnectionParameters(
                host=settings.rabbitmq_host, 
                port=settings.rabbitmq_port, 
                virtual_host=settings.rabbitmq_vhost, 
                credentials=credentials
            )

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            self.channel.exchange_declare(exchange=settings.orders_exchange, exchange_type='topic', durable=True)
            
            # Declare queues
            self.channel.queue_declare(queue=settings.payment_queue, durable=True)
            self.channel.queue_declare(queue=settings.notification_queue, durable=True)
            
            self.channel.queue_bind(
                exchange=settings.orders_exchange, 
                queue=settings.payment_queue,
                routing_key='order.created'
            )
             
            self.channel.queue_bind(
                exchange=settings.orders_exchange, 
                queue=settings.notification_queue,
                routing_key='order.*'
            )

        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            raise 

    def publish_message(self, routing_key: str, message: Dict[str, Any]):
        
        try: 
            
            if not self.connection or self.connection.is_closed:
                self._connect()

            message_body = json.dumps(message, default=str)
                
            self.channel.basic_publish(
                exchange=settings.orders_exchange,
                routing_key=routing_key, 
                body=message_body, 
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json', 
                    timestamp=int(message.get('created_at', 0))
                )
            )    
            
            print(f"Message published to {routing_key}: {message}")   
    
        except Exception as e: 
            print(f"Failed to publish message: {e}")
            
            try: 
                self._connect()
                self.channel.basic_publish(
                    exchange=settings.orders_exchange,
                    routing_key=routing_key, 
                    body=message_body, 
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        content_type='application/json', 
                        timestamp=int(message.get('created_at', 0))
                    )
                )    

                print(f"Message published to {routing_key}: {message}")   
            
            except Exception as retry_error: 
                print(f"Retry failed: {retry_error}")
            
            
    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()