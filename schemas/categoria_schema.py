from pydantic import BaseModel
from typing import Optional


class CategoriaCrear(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class CategoriaActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class CategoriaRespuesta(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: Optional[str] = None