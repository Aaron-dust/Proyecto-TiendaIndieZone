from pydantic import (
    BaseModel,
    field_validator
)

class DetalleVentaCrear(BaseModel):
    id_venta: int
    id_producto: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    @field_validator("cantidad")
    @classmethod
    def validar_cantidad(
        cls,
        valor
    ):
        if valor <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero"
            )
        return valor

    @field_validator("precio_unitario")
    @classmethod
    def validar_precio(
        cls,
        valor
    ):
        if valor <= 0:
            raise ValueError(
                "El precio unitario debe ser mayor que cero"
            )
        return valor

    @field_validator("subtotal")
    @classmethod
    def validar_subtotal(
        cls,
        valor
    ):
        if valor <= 0:
            raise ValueError(
                "El subtotal debe ser mayor que cero"
            )
        return valor

class DetalleVentaRespuesta(BaseModel):
    id_venta: int
    id_producto: int
    cantidad: int
    precio_unitario: float
    subtotal: float
