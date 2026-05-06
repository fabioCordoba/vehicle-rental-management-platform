## Estructura con microservicio:

```
sistema-alquiler-vehiculos/
│
├── microservicio-vehiculos/          ← Proyecto Django 1 (Puerto 8001)
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── vehiculos_project/
│   └── vehiculos_app/
│
├── microservicio-operaciones/        ← Proyecto Django 2 (Puerto 8002)
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── operaciones_project/
│   └── operaciones_app/
│
├── microservicio-usuarios/           ← Proyecto Django 3 (Puerto 8003)
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── usuarios_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── usuarios_app/
│       ├── models.py (Usuario, Perfil, etc.)
│       ├── views.py (Crear usuario, autenticación, etc.)
│       ├── serializers.py
│       └── urls.py
│
├── gateway/                          ← API Gateway (Puerto 8000)
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── ...
│
├── docker-compose.yml                ← Orquesta todo
└── README.md
```

## Flujo de comunicación actualizado:

```
Cliente HTTP
    ↓
API Gateway (8000)
    ├─→ /usuarios/*      → Microservicio Usuarios (8003)
    ├─→ /vehiculos/*     → Microservicio Vehículos (8001)
    └─→ /operaciones/*   → Microservicio Operaciones (8002)
         └─→ (Consulta Usuarios y Vehículos internamente)
```

## Funcionalidades del microservicio "usuarios":

```
CRUD de Usuarios:
├── POST   /usuarios/              → Crear usuario
├── GET    /usuarios/{id}          → Obtener usuario
├── PUT    /usuarios/{id}          → Actualizar usuario
├── DELETE /usuarios/{id}          → Eliminar usuario
│
Búsqueda:
├── GET    /usuarios/?email=...    → Buscar por email
├── GET    /usuarios/?cedula=...   → Buscar por cédula
│
Autenticación:
├── POST   /usuarios/login/        → Autenticar usuario
├── POST   /usuarios/logout/       → Cerrar sesión
└── POST   /usuarios/validate-token/ → Validar token
```

## Relaciones entre microservicios:

```
Operaciones:
  └─→ Consulta Usuarios (para verificar si existe)
  └─→ Consulta Vehículos (para validar disponibilidad)

Usuarios:
  └─→ Independiente (no depende de otros)

Vehículos:
  └─→ Independiente (no depende de otros)

Gateway:
  └─→ Solo redirige peticiones (no lógica de negocio)
```

**Resumen: Cada microservicio = 1 Proyecto Django + 1 Base de datos + 1 Contenedor Docker**
