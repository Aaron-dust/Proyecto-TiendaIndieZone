# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.base_datos import inicializar

from routers import (
    clientes,
    categorias,
    ofertas,
    productos,
    ventas,
    detalle_ventas
)

app = FastAPI(
    title="Sistema de Gestión TiendaIndieZone",
    version="1.0",
    description="API para gestionar la tienda"
)

# Permite que React se conecte con FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Revisa la conexión con PostgreSQL.
inicializar()

# Se agregan las rutas del sistema.
app.include_router(clientes.router)

app.include_router(categorias.router)

app.include_router(ofertas.router)

app.include_router(productos.router)

app.include_router(ventas.router)

app.include_router(detalle_ventas.router)

@app.get("/")
def inicio():
    return {
        "mensaje":
            "API Sistema de Gestión TiendaIndieZone",
        "version": "1.0",
        "docs": "/docs"
    }
