from pydantic import BaseModel, field_validator


class VentaCrear(BaseModel):
    fecha_venta: str
    total_venta: float
    id_cliente: int

    @field_validator("total_venta")
    @classmethod
    def validar_total(cls, valor):
        if valor <= 0:
            raise ValueError("El total de la venta debe ser mayor que cero")
        return valor


class VentaRespuesta(BaseModel):
    id_venta: int
    fecha_venta: str
    total_venta: float
    id_cliente: int