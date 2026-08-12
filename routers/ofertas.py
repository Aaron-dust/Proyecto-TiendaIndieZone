from fastapi import APIRouter, HTTPException
from dao.oferta_dao import (
    OfertaDAO,
    OfertaNoEncontradaError,
    OfertaDuplicadaError,
    OfertaConProductosError
)
from modelos.oferta import Oferta
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

@router.get("/",response_model=list[OfertaRespuesta])
def listar_ofertas():
    return [
        oferta.to_dict()
        for oferta in dao.obtener_todos()
    ]

@router.get("/{oferta_id}",response_model=OfertaRespuesta)
def obtener_oferta(oferta_id: int):
    oferta = dao.buscar_por_id(oferta_id)
    if not oferta:
        raise HTTPException(
            status_code=404,
            detail=f"Oferta ID={oferta_id} no encontrada"
        )
    return oferta.to_dict()

@router.post("/", response_model=OfertaRespuesta,status_code=201)
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
    except OfertaDuplicadaError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )

@router.put("/{oferta_id}", response_model=OfertaRespuesta)
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
    except OfertaNoEncontradaError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )
    except OfertaDuplicadaError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )

@router.delete("/{oferta_id}")
def eliminar_oferta(oferta_id: int):
    try:
        dao.eliminar(oferta_id)
        return {
            "mensaje": f"Oferta ID={oferta_id} eliminada"
        }
    except OfertaNoEncontradaError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )
    except OfertaConProductosError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
