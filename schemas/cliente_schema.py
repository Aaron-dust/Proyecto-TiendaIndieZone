import re
from pydantic import BaseModel, field_validator
from typing import Optional

class ClienteCrear(BaseModel):
    nombre: str
    apellido: str
    dni: str
    correo: str
    telefono: str
    fecha_registro: str
    @field_validator("dni")
    @classmethod
    def validar_dni(cls, valor):
        if not re.fullmatch(r"\d{8}", valor):
            raise ValueError("El DNI debe tener exactamente 8 dígitos numéricos")
        return valor

class ClienteActualizar(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    fecha_registro: Optional[str] = None

    @field_validator("dni")
    @classmethod
    def validar_dni(cls, valor):
        if valor is not None and not re.fullmatch(r"\d{8}", valor):
            raise ValueError("El DNI debe tener exactamente 8 dígitos numéricos")
        return valor

class ClienteRespuesta(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    dni: str
    correo: str
    telefono: str
    fecha_registro: str