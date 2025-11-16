"""Tests de la API"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    """
    Sobrescribe la función get_db para usar la base de datos de prueba
    
    yield una sesión de la base de datos de prueba, que se cierra automáticamente
    al finalizar el test
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    """Limpiar BD antes de cada test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

# TEST 1: Health check
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# TEST 2: Lista vacía inicial
def test_listar_contactos_vacio():
    response = client.get("/contactos")
    assert response.status_code == 200
    assert response.json() == []

# TEST 3: Crear contacto exitosamente
def test_crear_contacto():
    data = {
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "telefono": "+54 299 123456"
    }
    response = client.post("/contactos", json=data)
    assert response.status_code == 201
    assert response.json()["nombre"] == "Juan Pérez"
    assert "id" in response.json()

# TEST 4: Error sin nombre (campo requerido)
def test_crear_sin_nombre():
    data = {"email": "test@example.com"}
    response = client.post("/contactos", json=data)
    assert response.status_code == 422

# TEST 5: Email duplicado
def test_email_duplicado():
    data = {"nombre": "Test", "email": "duplicado@example.com"}
    client.post("/contactos", json=data)
    response = client.post("/contactos", json=data)
    assert response.status_code == 400

# TEST 6: Búsqueda de contactos
def test_buscar_contactos():
    # Crear contactos
    client.post("/contactos", json={"nombre": "Juan DevOps"})
    client.post("/contactos", json={"nombre": "María Backend"})
    
    # Buscar
    response = client.get("/contactos?search=Juan")
    assert response.status_code == 200
    assert len(response.json()) == 1

# TEST 7: Endpoint de búsqueda específico
def test_buscar_endpoint():
    client.post("/contactos", json={"nombre": "Pedro", "empresa": "ITS"})
    
    response = client.get("/contactos/buscar?q=ITS")
    assert response.status_code == 200
    assert len(response.json()) == 1