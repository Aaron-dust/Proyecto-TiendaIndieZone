# schemas/producto_schema.py

from typing import Optional
from pydantic import BaseModel, field_validator

class ProductoCrear(BaseModel):
    nombre_producto: str
    tipo_producto: str
    descripcion_producto: Optional[str] = None
    precio: float
    stock: int
    id_categoria: int
    id_oferta: Optional[int] = None
    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor):
        if valor <= 0:
            raise ValueError(
                "El precio debe ser mayor que cero"
            )
        return valor
        
    @field_validator("stock")
    @classmethod
    def validar_stock(cls, valor):
        if valor < 0:
            raise ValueError(
                "El stock no puede ser negativo"
            )
        return valor

class ProductoActualizar(BaseModel):
    nombre_producto: Optional[str] = None
    tipo_producto: Optional[str] = None
    descripcion_producto: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    id_categoria: Optional[int] = None
    id_oferta: Optional[int] = None

class ProductoRespuesta(BaseModel):
    id_producto: int
    nombre_producto: str
    tipo_producto: str
    descripcion_producto: Optional[str] = None
    precio: float
    stock: int
    id_categoria: int
    id_oferta: Optional[int] = None
