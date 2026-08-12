# routers/categorias.py

from fastapi import APIRouter, HTTPException

from modelos.categoria import Categoria

from dao.categoria_dao import (
    CategoriaDAO,
    CategoriaNoEncontradaError,
    CategoriaDuplicadaError,
    CategoriaConProductosError
)

from schemas.categoria_schema import (
    CategoriaCrear,
    CategoriaActualizar,
    CategoriaRespuesta
)

# Este router contiene todas las rutas relacionadas con las categorías.
router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)
dao = CategoriaDAO()

# LISTAR TODAS LAS CATEGORÍAS
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

# OBTENER CATEGORÍA POR ID
@router.get(
    "/{categoria_id}",
    response_model=CategoriaRespuesta
)
def obtener_categoria(
    categoria_id: int
):
    categoria = dao.buscar_por_id(
        categoria_id
    )
    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )
    return categoria.to_dict()

# CREAR CATEGORÍA
@router.post(
    "/",
    response_model=CategoriaRespuesta,
    status_code=201
)
def crear_categoria(
    datos: CategoriaCrear
):
    try:
        categoria = Categoria(
            datos.nombre,
            datos.descripcion
        )
        categoria = dao.insertar(
            categoria
        )
        return categoria.to_dict()
    except CategoriaDuplicadaError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

# ACTUALIZAR CATEGORÍA
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
            categoria_id,
            datos.nombre,
            datos.descripcion
        )

        return categoria.to_dict()

    except CategoriaNoEncontradaError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except CategoriaDuplicadaError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

# ELIMINAR CATEGORÍA
@router.delete(
    "/{categoria_id}"
)
def eliminar_categoria(
    categoria_id: int
):
    try:
        dao.eliminar(
            categoria_id
        )
        return {
            "mensaje":
                "Categoría eliminada correctamente"
        }
    except CategoriaNoEncontradaError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except CategoriaConProductosError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
