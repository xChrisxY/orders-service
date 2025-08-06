# Orders Service - Sistema de Pedidos Distribuido

Microservicio de órdenes construido con **FastAPI** y **arquitectura hexagonal** para un sistema tipo Uber Eats/Rappi.

## 🏗️ Arquitectura

Este proyecto implementa **Clean Architecture** (Arquitectura Hexagonal) con las siguientes capas:

```
📁 app/
├── 📁 config/          # Configuración de la aplicación
├── 📁 shared/          # Utilidades compartidas
└── 📁 orders/          # Dominio de órdenes
    ├── 📁 domain/      # Entidades, repositorios abstractos, servicios de dominio
    ├── 📁 application/ # Casos de uso, DTOs, eventos
    └── 📁 infrastructure/ # Implementaciones concretas, controladores, routers
```

## 🚀 Características

- ✅ **FastAPI** con documentación automática
- ✅ **MongoDB** como base de datos principal
- ✅ **RabbitMQ** para mensajería entre microservicios
- ✅ **Docker** y **Docker Compose** para containerización
- ✅ **Arquitectura Hexagonal** (Clean Architecture)
- ✅ **Patrón SAGA** mediante eventos
- ✅ **Manejo de errores** centralizado
- ✅ **Validaciones** con Pydantic
- ✅ **Health checks**
- ✅ **Logging** estructurado

## 🛠️ Tecnologías

- **FastAPI** 0.104.1
- **Motor** (MongoDB async driver)
- **Pika** (RabbitMQ client)
- **Pydantic** (validación de datos)
- **Docker** & **Docker Compose**

## 📋 Requisitos Previos

- Docker & Docker Compose
- Python 3.11+ (para desarrollo local)

## 🚀 Inicio Rápido

### 1. Clonar y configurar

```bash
# Copiar variables de entorno
cp .env.example .env

# Editar .env con tus configuraciones si es necesario
```

### 2. Ejecutar con Docker Compose

```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f orders-service
```

### 3. Verificar instalación

- **API Docs:** http://localhost:8001/docs
- **RabbitMQ Management:** http://localhost:15672 (admin/admin123)
- **Health Check:** http://localhost:8001/health

## 📚 Endpoints Principales

### Crear Orden
```http
POST /api/v1/orders/
Content-Type: application/json

{
  "user_id": "6571234567890abcdef12345",
  "restaurant_id": "6571234567890abcdef67890",
  "items": [
    {
      "product_id": "6571234567890abcdef11111",
      "product_name": "Pizza Margherita",
      "quantity": 2,
      "unit_price": 150.0
    }
  ],
  "delivery_address": {
    "street": "Av. Revolución 123",
    "city": "Ciudad de México",
    "state": "CDMX",
    "postal_code": "06700",
    "country": "Mexico"
  },
  "delivery_fee": 25.0,
  "tax_rate": 0.16
}
```

### Obtener Orden
```http
GET /api/v1/orders/{order_id}
```

### Órdenes por Usuario
```http
GET /api/v1/orders/user/{user_id}?page=1&per_page=10
```

### Actualizar Estado
```http
PATCH /api/v1/orders/{order_id}/status
Content-Type: application/json

{
  "new_status": "confirmed"
}
```

## 🔄 Estados de Orden

- `pending` → `confirmed` → `preparing` → `ready` → `in_delivery` → `delivered`
- `cancelled` (desde pending, confirmed, preparing)

## 📨 Eventos SAGA

El servicio publica eventos para el patrón SAGA:

1. **`order.created`** → Envía a cola `payment_requests`
2. **`order.status_changed`** → Envía a cola `notification_requests`

## 🗄️ Base de Datos

### Colección `orders`
```javascript
{
  _id: ObjectId,
  user_id: String,
  restaurant_id: String,
  items: [OrderItem],
  delivery_address: DeliveryAddress,
  status: String,
  total_amount: Number,
  delivery_fee: Number,
  tax_amount: Number,
  final_amount: Number,
  created_at: Date,
  updated_at: Date,
  estimated_delivery_time: Date
}
```

## 🧪 Testing

```bash
# Ejecutar tests unitarios
docker-compose exec orders-service pytest

# Con cobertura
docker-compose exec orders-service pytest --cov=app --cov-report=html
```

## 🔧 Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar MongoDB y RabbitMQ
docker-compose up -d mongodb rabbitmq redis

# Ejecutar aplicación
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📈 Monitoreo

- **Health Check:** `/health`
- **Metrics:** Implementar Prometheus + Grafana
- **Logs:** Centralizados con ELK Stack

## 🚀 Próximos Pasos

Para completar el sistema de pedidos distribuido:

1. **Payment Service** - Procesar pagos
2. **Notification Service** - Enviar notificaciones
3. **Delivery Service** - Gestionar repartidores
4. **API Gateway** - Kong/Nginx como puerta de entrada
5. **CI/CD Pipeline** - Jenkins para automatización

## 🤝 Contribuir

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agregar nueva característica'`)
4. Push al branch (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.