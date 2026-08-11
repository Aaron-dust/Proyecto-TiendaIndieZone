from pydantic import BaseModel
from typing import Optional
from datetime import date

class OfertaCrear(BaseModel):
    nombre: str
    porcentaje_descuento: float
    fecha_inicio: date
    fecha_fin: date

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
