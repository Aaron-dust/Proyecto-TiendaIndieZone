from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.base_datos import inicializar
from routers import (
    clientes,
    categorias,
    ofertas,
    productos,
    ventas,
    detalle_ventas,
    registros
)

app = FastAPI(
    title="Sistema de Gestión de TiendaIndieZone",
    version="1.0",
    description="API REST para la gestión de clientes, categorías, ofertas, productos y ventas"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

inicializar()

app.include_router(clientes.router)
app.include_router(categorias.router)
app.include_router(ofertas.router)
app.include_router(productos.router)
app.include_router(ventas.router)
app.include_router(detalle_ventas.router)
app.include_router(registros.router)

@app.get("/")
def inicio():
    return {
        "mensaje": "API Sistema de Gestión de TiendaIndieZone",
        "version": "1.0",
        "docs": "/docs"
    }