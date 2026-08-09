from fastapi import APIRouter, HTTPException
from dao.venta_dao import (
    VentaDAO,
    VentaNoEncontradaError
)
from dao.cliente_dao import (
    ClienteDAO
)
from modelos.venta import Venta
from schemas.venta_schema import (
    VentaCrear,
    VentaRespuesta
)
router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)
vdao = VentaDAO()
cdao = ClienteDAO()

@router.get("/", response_model=list[VentaRespuesta])
def listar_ventas():
    return [v.to_dict() for v in vdao.obtener_todos()]

@router.get("/{venta_id}", response_model=VentaRespuesta)
def obtener_venta(venta_id: int):
    v = vdao.buscar_por_id(venta_id)
    if not v:
        raise HTTPException(
            status_code=404,
            detail=f"Venta ID={venta_id} no encontrada"
        )
    return v.to_dict()

@router.post(
    "/",
    response_model=VentaRespuesta,
    status_code=201
)
def registrar_venta(datos: VentaCrear):
    cliente = cdao.buscar_por_id(datos.id_cliente)
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente ID={datos.id_cliente} no encontrado"
        )
    v = Venta(
        datos.fecha_venta,
        datos.total_venta,
        datos.id_cliente
    )
    v = vdao.insertar(v)
    return v.to_dict()

@router.get(
    "/cliente/{cliente_id}",
    response_model=list[VentaRespuesta]
)
def ventas_por_cliente(cliente_id: int):
    cliente = cdao.buscar_por_id(cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente ID={cliente_id} no encontrado"
        )
    ventas = [
        v for v in vdao.obtener_todos()
        if v.id_cliente == cliente_id
    ]
    return [v.to_dict() for v in ventas]