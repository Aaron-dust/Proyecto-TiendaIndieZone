# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten identificar errores específicos relacionados con la gestión
# de clientes sin utilizar excepciones genéricas.
# ----------------------------------------------------------------------------------
import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.cliente import Cliente


class ClienteNoEncontradoError(Exception):
    def __init__(self, cliente_id):
        super().__init__(f"Cliente ID={cliente_id} no encontrado")
class DNIDuplicadoError(Exception):
    def __init__(self, dni):
        super().__init__(f"DNI '{dni}' ya en el sistema ")
# Se genera cuando un cliente posee ventas registradas y no puede eliminarse.
class ClienteConVentasError(Exception):
    def __init__(self, cliente_id):
        super().__init__(
            f"Cliente ID={cliente_id} no se puede eliminar: tiene ventas registradas"
        )
# ---------------------------------------------------------------------------------
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
            INSERT INTO cliente
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
                %s, %s, %s, %s, %s, %s
            )
            RETURNING id_cliente
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
        # Guarda el id generado automáticamente.
        cliente.id = cursor.fetchone()["id_cliente"]
        conn.commit()
        conn.close()
        self._log.info(
            f"Cliente agregado: {cliente.nombre} {cliente.apellido} "
            f"(ID={cliente.id})"
        )
        return cliente

    def buscar_por_dni(self, dni):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # La coma convierte el parámetro en una tupla de un solo elemento.
        cursor.execute(
            """
            SELECT *
            FROM cliente
            WHERE dni = %s
            """,(dni,)
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
            FROM cliente
            WHERE id_cliente = %s
            """,(cliente_id,)
        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_cliente(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM cliente
            ORDER BY nombre
            """
        )
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
            UPDATE cliente
            SET
                nombre = %s,
                apellido = %s,
                dni = %s,
                correo = %s,
                telefono = %s,
                fecha_registro = %s
            WHERE id_cliente = %s
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
        self._log.info(
            f"Cliente actualizado: ID={cliente_id}"
        )
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
                DELETE FROM cliente
                WHERE id_cliente = %s
                """,
                (cliente_id,)
            )
            conn.commit()
            conn.close()
            self._log.info(
                f"Cliente eliminado: ID={cliente_id}"
            )
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            self._log.warning(
                f"Eliminar fallido: Cliente ID={cliente_id} "
                f"tiene ventas asociadas"
            )
            raise ClienteConVentasError(cliente_id)

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM cliente
            """
        )
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def _fila_a_cliente(self, fila):
        # Convierte una fila de PostgreSQL en un objeto Cliente.
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