# ----------------------------------------------------------------------------------
# ROUTER – Categorias
#
# Endpoints de FastAPI para gestionar las categorías.
# ----------------------------------------------------------------------------------

from fastapi import APIRouter, HTTPException
from dao.categoria_dao import (
    CategoriaDAO,
    CategoriaNoEncontradaError,
    CategoriaDuplicadaError,
    CategoriaConProductosError
)

from modelos.categoria import Categoria
from schemas.categoria_schema import (
    CategoriaCrear,
    CategoriaActualizar,
    CategoriaRespuesta
)

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)
dao = CategoriaDAO()

@router.get(
    "/",
    response_model=list[CategoriaRespuesta]
)
def listar_categorias():
    categorias = dao.obtener_todos()
    return [
        categoria.to_dict()
        for categoria in categorias
    ]

@router.get(
    "/{categoria_id}",
    response_model=CategoriaRespuesta
)
def obtener_categoria(categoria_id: int):
    categoria = dao.buscar_por_id(
        categoria_id
    )
    if not categoria:
        raise HTTPException(
            status_code=404,
            detail=f"Categoría ID={categoria_id} no encontrada"
        )
    return categoria.to_dict()

@router.post(
    "/",
    response_model=CategoriaRespuesta,
    status_code=201
)
def crear_categoria(datos: CategoriaCrear):
    try:
        categoria = Categoria(
            nombre=datos.nombre,
            descripcion=datos.descripcion
        )
        categoria = dao.insertar(
            categoria
        )
        return categoria.to_dict()
    except CategoriaDuplicadaError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )

@router.put(
    "/{categoria_id}",
    response_model=CategoriaRespuesta
)
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaActualizar
):
    try:
        categoria = dao.actualizar(
            categoria_id=categoria_id,
            nombre=datos.nombre,
            descripcion=datos.descripcion
        )

        return categoria.to_dict()
    except CategoriaNoEncontradaError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )
    except CategoriaDuplicadaError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )

@router.delete(
    "/{categoria_id}"
)
def eliminar_categoria(categoria_id: int):
    try:
        dao.eliminar(
            categoria_id
        )
        return {
            "mensaje": (
                f"Categoría ID={categoria_id} "
                f"eliminada correctamente"
            )
        }
    except CategoriaNoEncontradaError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )
    except CategoriaConProductosError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
