# schemas/oferta_schema.py

from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator

class OfertaCrear(BaseModel):
    nombre: str
    porcentaje_descuento: float
    fecha_inicio: date
    fecha_fin: date
    
    @field_validator("porcentaje_descuento")
    @classmethod
    def validar_descuento(cls, valor):
        if valor <= 0 or valor > 100:
            raise ValueError(
                "El descuento debe estar entre 1 y 100"
            )
        return valor

class OfertaActualizar(BaseModel):
    nombre: Optional[str] = None
    porcentaje_descuento: Optional[float] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class OfertaRespuesta(BaseModel):
    id_oferta: int
    nombre: str
    porcentaje_descuento: float
    fecha_inicio: date
    fecha_fin: date
