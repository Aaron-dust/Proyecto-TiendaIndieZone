# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten identificar errores específicos relacionados con la gestión
# de clientes sin utilizar excepciones genéricas.
# ----------------------------------------------------------------------------------
from config.logger import Logger
from config.base_datos import obtener_conexion
import sqlite3
from modelos.cliente import Cliente
class ClienteNoEncontradoError(Exception):
    def __init__(self, cliente_id):
        super().__init__(f"Cliente ID={cliente_id} no encontrado")

class DNIDuplicadoError(Exception):
    def __init__(self, dni):
        super().__init__(f"DNI '{dni}' ya registrado")

# Se genera cuando un cliente posee ventas registradas y no puede eliminarse.
class ClienteConVentasError(Exception):
    def __init__(self, cliente_id):
        super().__init__(
            f"Cliente ID={cliente_id} no se puede eliminar: tiene ventas asociadas"
        )
# ----------------------------------------------------------------------------------
# PATRÓN DAO – ClienteDAO
#
# Encapsula todas las operaciones relacionadas con la tabla Cliente.
# El resto del sistema interactúa únicamente mediante este DAO.
# ----------------------------------------------------------------------------------
class ClienteDAO:
    def __init__(self):
        self._log = Logger()
    def insertar(self, cliente):
        # Verifica que el DNI no exista previamente.
        if self.buscar_por_dni(cliente.dni):
            self._log.warning(f"DNI duplicado: {cliente.dni}")
            raise DNIDuplicadoError(cliente.dni)

        conn = obtener_conexion()
        cursor = conn.cursor()
        # Los parámetros se envían mediante placeholders para evitar inyección SQL.
        cursor.execute(
            """
            INSERT INTO Cliente
            (
                nombre,
                apellido,
                dni,
                correo,
                telefono,
                fecha_registro
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?
            )
            """,

            (
                cliente.nombre,
                cliente.apellido,
                cliente.dni,
                cliente.correo,
                cliente.telefono,
                cliente.fecha_registro
            )

        )
        conn.commit()
        # Guarda el id generado automáticamente.
        cliente.id = cursor.lastrowid
        conn.close()
        self._log.info(
            f"Cliente agregado: {cliente.nombre} {cliente.apellido} (ID={cliente.id})"
        )
        return cliente

    def buscar_por_dni(self, dni):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # La coma convierte el parámetro en una tupla de un solo elemento.
        cursor.execute(
            """
            SELECT *

            FROM Cliente

            WHERE dni = ?
            """,
            (dni,)
        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_cliente(fila) if fila else None

    def buscar_por_id(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(

            """
            SELECT *

            FROM Cliente

            WHERE id_cliente = ?
            """,

            (cliente_id,)
        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_cliente(fila) if fila else None
    # Elimina un cliente por ID
    def eliminar(self, id):
        cliente = self.buscar_por_id(id)
        if not cliente:

            self.__log.error(
                f"Eliminar fallido: Cliente ID={id} no existe"
            )

            raise ClienteNoEncontradoError(id)
        self.__bd.remove(cliente)
        self.__log.warning(
            f"Cliente eliminado: ID={id}"
        )