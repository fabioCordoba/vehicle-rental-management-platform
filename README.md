# Vehicle Rental Management Platform

Plataforma de gestión de alquiler de vehículos construida con arquitectura de microservicios. Cada servicio es una aplicación Django independiente que se comunica a través de un API Gateway Nginx.

---

## Arquitectura

```
Cliente
   │
   ▼
Nginx Gateway  (:8035 dev / :80 prod)
   ├── /api/authentication/  ──▶  authentication-service (:8000)
   ├── /api/users/           ──▶  authentication-service (:8000)
   ├── /api/transports/      ──▶  vehicle-service        (:8000)
   └── /api/procedures/      ──▶  operation-service      (:8000)
                                        │
                                        └── llama internamente a
                                            vehicle-service
PostgreSQL 14.3
   ├── authentication_db
   ├── vehicles_db
   └── operation_db
```

---

## Microservicios

### Authentication (`app-backend/authentication/`)

Gestión de usuarios, autenticación JWT y control de acceso.

| Método | Endpoint                               | Descripción                    |
| ------ | -------------------------------------- | ------------------------------ |
| POST   | `/api/authentication/register`         | Registro de usuario            |
| POST   | `/api/authentication/login/`           | Obtener tokens JWT             |
| POST   | `/api/authentication/refresh/`         | Renovar access token           |
| POST   | `/api/authentication/logout/`          | Cerrar sesión                  |
| POST   | `/api/authentication/logout_all/`      | Cerrar todas las sesiones      |
| POST   | `/api/authentication/forgot_password/` | Recuperar contraseña           |
| GET    | `/api/authentication/check-token/`     | Validar token                  |
| GET    | `/api/authentication/me`               | Perfil del usuario autenticado |
| POST   | `/api/authentication/change_pwd`       | Cambiar contraseña             |
| GET    | `/api/authentication/roles/`           | Roles disponibles              |
| CRUD   | `/api/users/`                          | Gestión de usuarios (admin)    |

### Vehicle (`app-backend/vehicle/`)

Gestión del inventario de vehículos. No interactúa con bases de datos externas; es consultado por otros microservicios.

| Método   | Endpoint                                    | Descripción                         |
| -------- | ------------------------------------------- | ----------------------------------- |
| GET/POST | `/api/transports/`                          | Listar / crear vehículos            |
| GET      | `/api/transports/{id}/`                     | Detalle de vehículo                 |
| PATCH    | `/api/transports/{id}/`                     | Actualizar vehículo (admin)         |
| DELETE   | `/api/transports/{id}/`                     | Soft delete (admin)                 |
| GET      | `/api/transports/available/`                | Solo vehículos disponibles          |
| GET      | `/api/transports/search/`                   | Búsqueda por marca, modelo y estado |
| GET      | `/api/transports/search-by-status/`         | Filtrar por disponibilidad          |
| PATCH    | `/api/transports/{id}/toggle-availability/` | Cambiar disponibilidad (admin)      |

**Parámetros de búsqueda** (`/api/transports/search/`):

| Parámetro | Tipo                        | Ejemplo             |
| --------- | --------------------------- | ------------------- |
| `make`    | string                      | `?make=toyota`      |
| `model`   | string                      | `?model=corolla`    |
| `status`  | `available` / `unavailable` | `?status=available` |

### Operation (`app-backend/operation/`)

Gestión del ciclo de vida de solicitudes de alquiler. Valida disponibilidad de vehículos consultando al microservicio `vehicle` y actualiza su estado al confirmar o cancelar.

| Método   | Endpoint                        | Descripción                                     |
| -------- | ------------------------------- | ----------------------------------------------- |
| GET/POST | `/api/procedures/`              | Listar / crear solicitudes                      |
| GET      | `/api/procedures/{id}/`         | Detalle de solicitud                            |
| PATCH    | `/api/procedures/{id}/`         | Actualizar solicitud                            |
| DELETE   | `/api/procedures/{id}/`         | Desactivar solicitud                            |
| PATCH    | `/api/procedures/{id}/confirm/` | Confirmar → marca vehículo no disponible        |
| PATCH    | `/api/procedures/{id}/cancel/`  | Cancelar → restaura disponibilidad del vehículo |

**Flujo de una solicitud:**

```
POST /api/procedures/        → valida vehículo disponible  → status: PENDING
PATCH .../confirm/           → toggle vehicle (no disponible) → status: ACTIVE
PATCH .../cancel/            → toggle vehicle (disponible)    → status: CANCELLED
```

---

## Stack tecnológico

| Componente        | Tecnología                                       |
| ----------------- | ------------------------------------------------ |
| Framework         | Django 5.2 + Django REST Framework               |
| ASGI Server       | Daphne                                           |
| Base de datos     | PostgreSQL 14.3                                  |
| Autenticación     | JWT (simplejwt) — stateless entre microservicios |
| Gateway           | Nginx 1.27                                       |
| Contenedores      | Docker + Docker Compose                          |
| Gestión de deps   | uv                                               |
| Documentación API | drf-spectacular (Swagger / ReDoc)                |

---

## Estructura del repositorio

```
vehicle-rental-management-platform/
├── app-backend/
│   ├── authentication/          # Microservicio de autenticación
│   │   ├── apps/
│   │   │   ├── authentication/
│   │   │   ├── users/
│   │   │   └── core/
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   └── pyproject.toml
│   ├── vehicle/                 # Microservicio de vehículos
│   │   ├── apps/
│   │   │   ├── transport/
│   │   │   └── core/
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   └── pyproject.toml
│   └── operation/               # Microservicio de operaciones
│       ├── apps/
│       │   ├── procedure/
│       │   └── core/
│       ├── Dockerfile
│       ├── entrypoint.sh
│       └── pyproject.toml
├── app-frontend/                # (pendiente)
└── docker/
    ├── docker-compose.yml       # Entorno de desarrollo
    ├── docker-compose.prod.yml  # Entorno de producción
    ├── .env                     # Variables de base de datos (desarrollo)
    ├── .env.prod.example        # Plantilla de variables de producción
    ├── init-db.sh               # Inicialización idempotente de bases de datos
    └── nginx/
        ├── nginx.conf
        ├── conf.d/
        │   └── gateway.conf     # Routing desarrollo
        └── conf.d.prod/
            └── gateway.prod.conf # Routing producción
```

---

## Inicio rápido — Desarrollo

### Requisitos

- Docker y Docker Compose
- Python 3.12+ (para desarrollo local sin Docker)
- uv

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd vehicle-rental-management-platform
```

### 2. Configurar variables de entorno

El archivo `docker/.env` ya incluye valores para desarrollo. Para personalizar:

```bash
cp docker/.env docker/.env.local
# editar según sea necesario
```

Cada microservicio tiene su propio `.env` en `app-backend/<servicio>/.env`.

### 3. Levantar con Docker Compose

```bash
cd docker
docker compose up --build -d
```

Servicios disponibles:

| Servicio          | URL                                                           |
| ----------------- | ------------------------------------------------------------- |
| API Gateway       | `http://localhost:8025`                                       |
| PostgreSQL        | `localhost:5440`                                              |
| Swagger Auth      | `http://localhost:8025/docs/auth/api/schema/swagger-ui/`      |
| Swagger Vehicle   | `http://localhost:8025/docs/vehicle/api/schema/swagger-ui/`   |
| Swagger Operation | `http://localhost:8025/docs/operation/api/schema/swagger-ui/` |
| Health check      | `http://localhost:8025/health`                                |

### 4. Desarrollo local (sin Docker)

Cada microservicio puede correrse de forma independiente:

```bash
cd app-backend/authentication
uv run python manage.py runserver 8000

cd app-backend/vehicle
uv run python manage.py runserver 8001

cd app-backend/operation
uv run python manage.py runserver 8002
```

Asegúrate de que `VEHICLE_SERVICE_URL=http://localhost:8001` esté configurado en `app-backend/operation/.env`.

---

## Despliegue en Producción

### 1. Preparar variables de entorno

```bash
cd docker
cp .env.prod.example .env.prod
# editar .env.prod con valores reales de producción
```

Variables requeridas en `.env.prod`:

```env
DATABASE_USER=<usuario>
DATABASE_PASSWD=<contraseña_fuerte>
AUTH_SECRET_KEY=<clave_aleatoria>      # python -c "import secrets; print(secrets.token_urlsafe(50))"
VEHICLE_SECRET_KEY=<clave_aleatoria>
OPERATION_SECRET_KEY=<clave_aleatoria>
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
CORS_ALLOWED_ORIGINS=https://tudominio.com
DOMAIN=tudominio.com
```

### 2. Publicar imágenes en Docker Hub

```bash
cd docker
docker compose build
docker login -u user
docker compose push
```

Imágenes publicadas:

- `fabiocordobadev/personal-authentication:latest`
- `fabiocordobadev/personal-vehicle:latest`
- `fabiocordobadev/personal-operation:latest`

### 3. Desplegar en el servidor

```bash
# En el servidor
cd docker
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### 4. Acceder a Swagger en producción (vía túnel SSH)

Los servicios exponen Swagger solo en `127.0.0.1` del servidor:

```bash
ssh -L 9000:localhost:9000 \
    -L 9001:localhost:9001 \
    -L 9002:localhost:9002 \
    usuario@tudominio.com
```

| Servicio       | URL local                                      |
| -------------- | ---------------------------------------------- |
| Authentication | `http://localhost:9000/api/schema/swagger-ui/` |
| Vehicle        | `http://localhost:9001/api/schema/swagger-ui/` |
| Operation      | `http://localhost:9002/api/schema/swagger-ui/` |

---

## Variables de entorno por microservicio

| Variable               | Descripción                                                                   |
| ---------------------- | ----------------------------------------------------------------------------- |
| `SECRET_KEY`           | Clave secreta Django (debe ser igual en todos los servicios para validar JWT) |
| `DEBUG`                | `True` desarrollo / `False` producción                                        |
| `ALLOWED_HOSTS`        | Hosts permitidos separados por coma                                           |
| `DB_ENGINE`            | `django.db.backends.postgresql`                                               |
| `DB_NAME`              | Nombre de la base de datos del servicio                                       |
| `DB_USER`              | Usuario de PostgreSQL                                                         |
| `DB_PASSWORD`          | Contraseña de PostgreSQL                                                      |
| `DB_HOST`              | Host de PostgreSQL (`localhost` dev / `postgres-db` Docker)                   |
| `DB_PORT`              | Puerto PostgreSQL (`5440` dev / `5432` Docker interno)                        |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para CORS                                                 |
| `VEHICLE_SERVICE_URL`  | _(Solo operation)_ URL del microservicio de vehículos                         |

---

## Comunicación entre microservicios

```
operation-service
   │
   ├── POST /api/procedures/
   │       └── GET  vehicle-service/api/transports/{id}/       (valida disponibilidad)
   │
   ├── PATCH .../confirm/
   │       └── PATCH vehicle-service/api/transports/{id}/toggle-availability/
   │
   └── PATCH .../cancel/
           └── PATCH vehicle-service/api/transports/{id}/toggle-availability/  (si era ACTIVE)
```

Todos los servicios validan tokens JWT usando la misma `SECRET_KEY`. El token emitido por `authentication-service` es válido en `vehicle-service` y `operation-service` sin consultar la base de datos (validación stateless).

---

## Comandos útiles

```bash
# Ver estado de los contenedores
docker compose ps

# Ver logs de un servicio
docker compose logs -f vehicle-service

# Ejecutar migraciones manualmente
docker exec vehicle-rental-vehicle uv run python manage.py migrate

# Acceder a la shell de Django
docker exec -it vehicle-rental-vehicle uv run python manage.py shell

# Reiniciar un servicio
docker compose restart vehicle-service

# Reconstruir y reiniciar
docker compose up --build -d vehicle-service
```
