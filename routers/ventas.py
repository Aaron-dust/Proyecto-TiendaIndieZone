from fastapi import APIRouter, HTTPException
from dao.venta_dao import (
    VentaDAO,
    VentaNoEncontradaError
)

from dao.cliente_dao import ClienteDAO
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

@router.get(
    "/",
    response_model=list[VentaRespuesta]
)
def listar_ventas():
    return [
        venta.to_dict()
        for venta in vdao.obtener_todos()
    ]

@router.get(
    "/{venta_id}",
    response_model=VentaRespuesta
)
def obtener_venta(venta_id: int):
    venta = vdao.buscar_por_id(
        venta_id
    )
    if not venta:
        raise HTTPException(
            status_code=404,
            detail=f"Venta ID={venta_id} no encontrada"
        )
    return venta.to_dict()

@router.post(
    "/",
    response_model=VentaRespuesta,
    status_code=201
)
def registrar_venta(datos: VentaCrear):
    cliente = cdao.buscar_por_id(
        datos.id_cliente
    )
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente ID={datos.id_cliente} no encontrado"
        )
    venta = Venta(
        datos.fecha_venta,
        datos.total_venta,
        datos.id_cliente
    )
    venta = vdao.insertar(
        venta
    )
    return venta.to_dict()

@router.get(
    "/cliente/{cliente_id}",
    response_model=list[VentaRespuesta]
)
def ventas_por_cliente(cliente_id: int):
    cliente = cdao.buscar_por_id(
        cliente_id
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente ID={cliente_id} no encontrado"
        )
    ventas = [
        venta
        for venta in vdao.obtener_todos()
        if venta.id_cliente == cliente_id
    ]
    return [
        venta.to_dict()
        for venta in ventas
    ]
