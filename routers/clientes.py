from fastapi import APIRouter, HTTPException

from dao.cliente_dao import (
    ClienteDAO,
    ClienteNoEncontradoError,
    DNIDuplicadoError,
    ClienteConVentasError
)

from modelos.cliente import Cliente

from schemas.cliente_schema import (
    ClienteCrear,
    ClienteActualizar,
    ClienteRespuesta
)
router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)
dao = ClienteDAO()

# Lista clientes y también permite realizar búsquedas.
@router.get(
    "/",
    response_model=list[ClienteRespuesta]
)
def listar_clientes(
    dni: str | None = None,
    nombre: str | None = None,
    correo: str | None = None
):
    
    # Si se escribe algún dato, se realiza una búsqueda.
    if dni or nombre or correo:

        clientes = dao.buscar(
            dni=dni,
            nombre=nombre,
            correo=correo
        )

    # Si no se escribe nada, muestra todos.
    else:
        clientes = dao.obtener_todos()
    return [
        cliente.to_dict()
        for cliente in clientes
    ]

@router.post(
    "/",
    response_model=ClienteRespuesta,
    status_code=201
)
def crear_cliente(
    datos: ClienteCrear
):
    try:
        cliente = Cliente(
            datos.nombre,
            datos.apellido,
            datos.dni,
            datos.correo,
            datos.telefono,
            datos.fecha_registro
        )
        cliente = dao.insertar(
            cliente
        )
        return cliente.to_dict()
    except DNIDuplicadoError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.get(
    "/{cliente_id}",
    response_model=ClienteRespuesta
)
def obtener_cliente(
    cliente_id: int
):
    cliente = dao.buscar_por_id(
        cliente_id
    )
    if not cliente:

        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )
    return cliente.to_dict()

@router.put(
    "/{cliente_id}",
    response_model=ClienteRespuesta
)
def actualizar_cliente(
    cliente_id: int,
    datos: ClienteActualizar
):
    try:
        cliente = dao.actualizar(
            cliente_id,
            datos.nombre,
            datos.apellido,
            datos.dni,
            datos.correo,
            datos.telefono,
            datos.fecha_registro
        )

        return cliente.to_dict()
    except ClienteNoEncontradoError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except DNIDuplicadoError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.delete(
    "/{cliente_id}"
)
def eliminar_cliente(
    cliente_id: int
):
    try:
        dao.eliminar(
            cliente_id
        )
        return {
            "mensaje":
                "Cliente eliminado correctamente"
        }
    except ClienteNoEncontradoError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except ClienteConVentasError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
