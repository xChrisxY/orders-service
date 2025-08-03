from pydantic_settings import BaseSettings 
from typing import Optional 

class Settings(BaseSettings): 
    
    # Application settings
    app_name: str = "Orders Service"
    debug: bool = False 
    version: str = "1.0.0"
    
    # Database settings 
    mongo_url: str = "mongodb://localhost:27017" 
    database_name: str = "orders_db"
    
    # RabbitMQ settings 
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672 
    rabbitmq_username: str = "guest"
    rabbitmq_password: str = "guest"
    rabbitmq_vhost: str = "/"
    
    # Exchange and Queue settings 
    orders_exchange: str = "orders_exchange"
    payment_queue: str = "payment_requests"
    notification_queue: str = "notification_requests"
    
    # JWT settings 
    secret_key: str = "my-secret-key" 
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30 
    
    # CORS settings 
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config: 
        env_file = ".env"
        
settings = Settings()
    
    
    