from pydantic import BaseModel, field_validator
from typing import Optional


class OfertaCrear(BaseModel):
    nombre: str
    porcentaje_descuento: float
    fecha_inicio: str
    fecha_fin: str
    @field_validator("porcentaje_descuento")
    @classmethod
    def validar_descuento(cls, valor):
        if valor < 0 or valor > 100:
            raise ValueError(
                "El porcentaje de descuento debe estar entre 0 y 100"
            )
        return valor

class OfertaActualizar(BaseModel):
    nombre: Optional[str] = None
    porcentaje_descuento: Optional[float] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None

    @field_validator("porcentaje_descuento")
    @classmethod
    def validar_descuento(cls, valor):
        if valor is not None and (valor < 0 or valor > 100):
            raise ValueError(
                "El porcentaje de descuento debe estar entre 0 y 100"
            )
        return valor

class OfertaRespuesta(BaseModel):
    id_oferta: int
    nombre: str
    porcentaje_descuento: float
    fecha_inicio: str
    fecha_fin: str