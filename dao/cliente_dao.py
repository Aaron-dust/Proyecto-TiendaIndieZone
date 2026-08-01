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
    def obtener_todos(self):

        conn = obtener_conexion()
        cursor = conn.cursor()
        # SQLite realiza el ordenamiento de los registros.
        cursor.execute("""
            SELECT *

            FROM Cliente

            ORDER BY nombre
        """)
        filas = cursor.fetchall()
        conn.close()
        # Convierte cada fila de la BD en un objeto Cliente.
        return [self._fila_a_cliente(f) for f in filas]

    def actualizar(
        self,
        cliente_id,
        nombre=None,
        apellido=None,
        dni=None,
        correo=None,
        telefono=None,
        fecha_registro=None
    ):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self._log.error(
                f"Actualizar fallido: Cliente ID={cliente_id} no existe"
            )
            raise ClienteNoEncontradoError(cliente_id)

        # Conserva el valor actual cuando un campo no es enviado.
        nuevo_nombre = nombre if nombre is not None else c.nombre
        nuevo_apellido = apellido if apellido is not None else c.apellido
        nuevo_dni = dni if dni is not None else c.dni
        nuevo_correo = correo if correo is not None else c.correo
        nuevo_telefono = telefono if telefono is not None else c.telefono
        nueva_fecha = (
            fecha_registro
            if fecha_registro is not None
            else c.fecha_registro
        )

        # Verifica que el nuevo DNI no pertenezca a otro cliente.
        cliente_dni = self.buscar_por_dni(nuevo_dni)

        if cliente_dni and cliente_dni.id != cliente_id:
            self._log.warning(f"DNI duplicado: {nuevo_dni}")
            raise DNIDuplicadoError(nuevo_dni)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(

            """
            UPDATE Cliente
            SET
                nombre = ?,
                apellido = ?,
                dni = ?,
                correo = ?,
                telefono = ?,
                fecha_registro = ?
            WHERE id_cliente = ?
            """,

            (
                nuevo_nombre,
                nuevo_apellido,
                nuevo_dni,
                nuevo_correo,
                nuevo_telefono,
                nueva_fecha,
                cliente_id
            )

        )
        conn.commit()
        conn.close()
        c.nombre = nuevo_nombre
        c.apellido = nuevo_apellido
        c.dni = nuevo_dni
        c.correo = nuevo_correo
        c.telefono = nuevo_telefono
        c.fecha_registro = nueva_fecha

        self._log.info(f"Cliente actualizado: ID={cliente_id}")
        return c

    def eliminar(self, cliente_id):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self._log.error(
                f"Eliminar fallido: Cliente ID={cliente_id} no existe"
            )
            raise ClienteNoEncontradoError(cliente_id)
        conn = obtener_conexion()
        cursor = conn.cursor()

        try:

            # La clave foránea impide eliminar clientes con ventas.
            cursor.execute(

                """
                DELETE FROM Cliente
                WHERE id_cliente = ?
                """,
                (cliente_id,)

            )

            conn.commit()
            conn.close()
            self._log.info(f"Cliente eliminado: ID={cliente_id}")

        except sqlite3.IntegrityError:

            conn.close()
            self._log.warning(
                f"Eliminar fallido: Cliente ID={cliente_id} tiene ventas asociadas"
            )
            raise ClienteConVentasError(cliente_id)

    def total(self):

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(

            """
            SELECT COUNT(*)
            FROM Cliente

            """

        )

        total = cursor.fetchone()[0]
        conn.close()
        return total

    def _fila_a_cliente(self, fila):
        # Convierte una fila de SQLite en un objeto Cliente.
        c = Cliente(
            fila["nombre"],
            fila["apellido"],
            fila["dni"],
            fila["correo"],
            fila["telefono"],
            fila["fecha_registro"]

        )

        c.id = fila["id_cliente"]

        return c