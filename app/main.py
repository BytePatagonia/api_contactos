"""API de Contactos - Versión Minimalista"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db, Base
from .models import Contacto
from .schemas import ContactoCreate, ContactoResponse

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Contactos", version="1.0.0")

# ENDPOINT 1: Health Check
@app.get("/health")
def health_check():
    """Verifica que la API esté funcionando"""
    return {
        "status": "healthy",
        "service": "API Contactos",
        "version": "1.0.0"
    }

# ENDPOINT 2: Listar contactos (con búsqueda opcional)
@app.get("/contactos", response_model=List[ContactoResponse])
def listar_contactos(
    search: str = None,
    db: Session = Depends(get_db)
):
    """
    Lista todos los contactos
    - search: Busca en nombre, email o empresa
    """
    query = db.query(Contacto)
    
    # Búsqueda opcional
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Contacto.nombre.ilike(search_filter)) |
            (Contacto.email.ilike(search_filter)) |
            (Contacto.empresa.ilike(search_filter))
        )
    
    return query.all()

# ENDPOINT 3: Crear contacto
@app.post(
    "/contactos",
    response_model=ContactoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_contacto(
    contacto: ContactoCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo contacto
    - nombre: requerido
    - email: opcional (no permite duplicados)
    """
    # Validar email duplicado
    if contacto.email:
        existe = db.query(Contacto).filter(
            Contacto.email == contacto.email
        ).first()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un contacto con el email {contacto.email}"
            )
    
    # Crear contacto
    db_contacto = Contacto(**contacto.model_dump())
    db.add(db_contacto)
    db.commit()
    db.refresh(db_contacto)
    
    return db_contacto

# ENDPOINT 4: Buscar por término
@app.get("/contactos/buscar", response_model=List[ContactoResponse])
def buscar_contactos(
    q: str,
    db: Session = Depends(get_db)
):
    """
    Busca contactos por nombre, email o empresa
    - q: término de búsqueda (requerido)
    """
    search_filter = f"%{q}%"
    return db.query(Contacto).filter(
        (Contacto.nombre.ilike(search_filter)) |
        (Contacto.email.ilike(search_filter)) |
        (Contacto.empresa.ilike(search_filter))
    ).all()
