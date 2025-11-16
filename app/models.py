"""Modelo de datos"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Contacto(Base):
    __tablename__ = "contactos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    telefono = Column(String(50), nullable=True)
    email = Column(String(200), nullable=True, index=True)
    empresa = Column(String(200), nullable=True)
    notas = Column(String(1000), nullable=True)
    es_favorito = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())