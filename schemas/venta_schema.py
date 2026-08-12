from pydantic import BaseModel
from typing import Optional
from datetime import date

class VentaCrear(BaseModel):
    fecha_venta: date
    total_venta: float
    id_cliente: int

class VentaActualizar(BaseModel):
    fecha_venta: Optional[date] = None
    total_venta: Optional[float] = None
    id_cliente: Optional[int] = None

class VentaRespuesta(BaseModel):
    id_venta: int
    fecha_venta: date
    total_venta: float
    id_cliente: int
