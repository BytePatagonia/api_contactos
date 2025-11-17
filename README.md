# 📇 API Contactos - Trabajo Final DevOps

API REST minimalista para gestión de contactos con FastAPI y PostgreSQL.

---

## 🚀 Inicio Rápido

### Requisitos
- Docker v24+
- Docker Compose v2+

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/BytePatagonia/api_contactos.git
cd api_contactos

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Levantar servicios
docker compose up --build

# 4. Verificar
# Abrir: http://localhost:8000/health
```

---

## 📌 Endpoints

### 1. Health Check
```http
GET /health
```

### 2. Listar Contactos
```http
GET /contactos
GET /contactos?search=Juan
```

### 3. Crear Contacto
```http
POST /contactos
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "+54 299 123456",
  "empresa": "ITS Cipolletti"
}
```

### 4. Buscar
```http
GET /contactos/buscar?q=ITS
```

---

## 🧪 Tests

```bash
# Con Docker
docker compose run --rm api pytest tests/ -v

# Sin Docker
pip install -r requirements.txt
pytest tests/ -v
```

**Tests incluidos (7):**
1. Health check
2. Lista vacía
3. Crear contacto
4. Validación nombre requerido
5. Email duplicado
6. Búsqueda en lista
7. Endpoint de búsqueda

---

## 📁 Estructura

```
api_contactos/
├── app/
│   ├── __init__.py
│   ├── main.py          # 4 endpoints
│   ├── database.py      # Configuración BD
│   ├── models.py        # Modelo Contacto
│   └── schemas.py       # Validación
├── tests/
│   ├── __init__.py
│   └── test_main.py     # 7 tests
├── .env.example         # Variables de entorno
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔐 Variables de Entorno

Archivo `.env`:
```env
POSTGRES_USER=xxxxx
POSTGRES_PASSWORD=xxxxx
POSTGRES_DB=xxxxx
API_PORT=8000
```

---

## 📊 CI/CD

GitHub Actions ejecuta automáticamente:
- ✅ Tests con pytest
- ✅ Build de imagen Docker

---

## 👨‍💻 Autor

**Muñoz Erika **  
ITS Cipolletti - Prácticas DevOps  
Noviembre 2024

---

## 📄 Licencia

Proyecto educativo - Código abierto