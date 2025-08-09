from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware 
from contextlib import asynccontextmanager 
import logging 

from .config.settings import settings 
from .config.database import connect_to_mongo, close_mongo_connection

from .orders.infraestructure.routers.order_router import router as orders_router 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager 
async def lifespan(app: FastAPI):
    
    logger.info("Starting Orders Service...")
    await connect_to_mongo()
    logger.info("Connect to MongoDB")
    
    yield 
    
    logger.info("Shutting down Orders Service...")
    await close_mongo_connection()
    logger.info("Disconnected from MongoDB")


app = FastAPI(
    title=settings.app_name, 
    description="Microservicio de órdenes para sistema de pedidos distribuido", 
    version=settings.version, 
    debug=settings.debug, 
    lifespan=lifespan,
    docs_url="/docs", 
    redoc_url="/redoc", 
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.allowed_origins, 
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"]
)

@app.get("/health", tags=["health"])
async def health_check(): 
    return {
        "status": "healthy", 
        "service": settings.app_name, 
        "version": settings.version
    }
    
@app.get("/", tags=["root"])
async def root():
    
    return {
        "message": f"Welcome to {settings.app_name}", 
        "version": settings.version, 
        "docs": "/docs"
    }
    
app.include_router(orders_router)

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=settings.debug, 
        log_level="info"
    )