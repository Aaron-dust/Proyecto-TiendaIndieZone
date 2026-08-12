# routers/ofertas.py

from fastapi import APIRouter, HTTPException

from modelos.oferta import Oferta

from dao.oferta_dao import (
    OfertaDAO,
    OfertaNoEncontradaError,
    OfertaDuplicadaError,
    OfertaConProductosError
)

from schemas.oferta_schema import (
    OfertaCrear,
    OfertaActualizar,
    OfertaRespuesta
)
router = APIRouter(
    prefix="/ofertas",
    tags=["Ofertas"]
)
dao = OfertaDAO()

# Lista todas las ofertas.
@router.get(
    "/",
    response_model=list[OfertaRespuesta]
)
def listar_ofertas():
    ofertas = dao.obtener_todos()
    return [
        oferta.to_dict()
        for oferta in ofertas
    ]

# Obtiene una oferta por ID.
@router.get(
    "/{oferta_id}",
    response_model=OfertaRespuesta
)
def obtener_oferta(oferta_id: int):
    oferta = dao.buscar_por_id(oferta_id)
    if not oferta:
        raise HTTPException(
            status_code=404,
            detail="Oferta no encontrada"
        )
    return oferta.to_dict()

# Crea una nueva oferta.
@router.post(
    "/",
    response_model=OfertaRespuesta,
    status_code=201
)
def crear_oferta(datos: OfertaCrear):
    try:
        oferta = Oferta(
            datos.nombre,
            datos.porcentaje_descuento,
            datos.fecha_inicio,
            datos.fecha_fin
        )
        oferta = dao.insertar(oferta)
        return oferta.to_dict()
    except OfertaDuplicadaError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

# Actualiza una oferta.
@router.put(
    "/{oferta_id}",
    response_model=OfertaRespuesta
)
def actualizar_oferta(
    oferta_id: int,
    datos: OfertaActualizar
):
    try:
        oferta = dao.actualizar(
            oferta_id,
            datos.nombre,
            datos.porcentaje_descuento,
            datos.fecha_inicio,
            datos.fecha_fin
        )
        return oferta.to_dict()
    except OfertaNoEncontradaError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except OfertaDuplicadaError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

# Elimina una oferta.
@router.delete(
    "/{oferta_id}"
)
def eliminar_oferta(oferta_id: int):
    try:
        dao.eliminar(oferta_id)
        return {
            "mensaje":
                "Oferta eliminada correctamente"
        }
    except OfertaNoEncontradaError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except OfertaConProductosError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
