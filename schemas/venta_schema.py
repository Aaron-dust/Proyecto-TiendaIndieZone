# schemas/venta_schema.py

from datetime import date
from pydantic import BaseModel, field_validator

class VentaCrear(BaseModel):
    fecha_venta: date
    total_venta: float
    id_cliente: int

    @field_validator("total_venta")
    @classmethod
    def validar_total(cls, valor):
        if valor <= 0:
            raise ValueError(
                "El total debe ser mayor que cero"
            )
        return valor

class VentaRespuesta(BaseModel):
    id_venta: int
    fecha_venta: date
    total_venta: float
    id_cliente: int

class VentaClienteResumen(BaseModel):
    id_cliente: int
    cliente: str
    cantidad_ventas: int
    total_comprado: float
    ventas: list[VentaRespuesta]
