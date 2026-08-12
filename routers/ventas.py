from fastapi import APIRouter, HTTPException

from modelos.venta import Venta

from dao.venta_dao import VentaDAO
from dao.cliente_dao import ClienteDAO

from schemas.venta_schema import (
    VentaCrear,
    VentaRespuesta,
    VentaClienteResumen
)

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)
vdao = VentaDAO()
cdao = ClienteDAO()

# Lista todas las ventas o busca las ventas de un cliente.
@router.get(
    "/",
    response_model=list[VentaRespuesta]
)
def listar_ventas(
    cliente_id: int | None = None
):

    # Si se coloca un cliente, muestra sus ventas.
    if cliente_id is not None:
        cliente = cdao.buscar_por_id(
            cliente_id
        )
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado"
            )
        ventas = vdao.buscar_por_cliente(
            cliente_id
        )

    # Si no se coloca cliente, muestra todas.
    else:
        ventas = vdao.obtener_todos()
    return [
        venta.to_dict()
        for venta in ventas
    ]

@router.post(
    "/",
    response_model=VentaRespuesta,
    status_code=201
)
def crear_venta(
    datos: VentaCrear
):
    cliente = cdao.buscar_por_id(
        datos.id_cliente
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
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

# Muestra el total comprado por un cliente.
@router.get(
    "/cliente/{cliente_id}/resumen",
    response_model=VentaClienteResumen
)
def resumen_cliente(
    cliente_id: int
):
    cliente = cdao.buscar_por_id(
        cliente_id
    )
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )
    ventas = vdao.buscar_por_cliente(
        cliente_id
    )
    resumen = vdao.resumen_por_cliente(
        cliente_id
    )

    return {
        "id_cliente":
            cliente_id,
        "cliente":
            f"{cliente.nombre} "
            f"{cliente.apellido}",
        "cantidad_ventas":
            resumen["cantidad_ventas"],

        "total_comprado":
            resumen["total_comprado"],
        "ventas":
            [
                venta.to_dict()
                for venta in ventas
            ]
    }

@router.get(
    "/{venta_id}",
    response_model=VentaRespuesta
)
def obtener_venta(
    venta_id: int
):
    venta = vdao.buscar_por_id(
        venta_id
    )

    if not venta:
        raise HTTPException(
            status_code=404,
            detail="Venta no encontrada"
        )
    return venta.to_dict()
