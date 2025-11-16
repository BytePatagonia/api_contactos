"""Esquemas de validación"""
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class ContactoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    telefono: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    empresa: Optional[str] = Field(None, max_length=200)
    notas: Optional[str] = Field(None, max_length=1000)
    es_favorito: bool = False

class ContactoResponse(BaseModel):
    id: int
    nombre: str
    telefono: Optional[str]
    email: Optional[str]
    empresa: Optional[str]
    notas: Optional[str]
    es_favorito: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}