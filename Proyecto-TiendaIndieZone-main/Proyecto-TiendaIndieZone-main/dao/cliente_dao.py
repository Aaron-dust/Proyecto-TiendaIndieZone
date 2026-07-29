import sqlite3
from config.base_datos import obtener_conexion
from config.logger import Logger
from modelos.cliente import Cliente

class ClienteNoEncontradoError(Exception):

    # crea el mensaje para un cliente inexistente.
    def __init__(self, id_cliente):
        super().__init__(
            f"No existe un cliente con ID={id_cliente}"
        )

class DNIDuplicadoError(Exception):

    # crea el mensaje para un DNI duplicado.
    def __init__(self, dni):
        super().__init__(
            f"Ya existe un cliente con el DNI {dni}"
        )

class ClienteConVentasError(Exception):

    # crea el mensaje cuando el cliente tiene ventas.
    def __init__(self, id_cliente):
        super().__init__(
            f"No se puede eliminar el cliente ID={id_cliente} "
            f"porque tiene ventas registradas"
        )

class ClienteDAO:

    # utiliza el historial compartido del sistema.
    def __init__(self):
        self.__log = Logger()

    # inserta un cliente en la base de datos.
    def insertar(self, cliente):
        if self.buscar_por_dni(cliente.dni):
            self.__log.warning(
                f"DNI duplicado: {cliente.dni}"
            )
            raise DNIDuplicadoError(cliente.dni)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
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
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """, (
            cliente.nombre,
            cliente.apellido,
            cliente.dni,
            cliente.correo,
            cliente.telefono,
            cliente.fecha_registro
        ))

        conexion.commit()
        cliente.id = cursor.lastrowid

        cursor.close()
        conexion.close()

        self.__log.info(
            f"Cliente agregado: "
            f"{cliente.nombre} {cliente.apellido} "
            f"(ID={cliente.id})"
        )

        return cliente

    # busca un cliente por su DNI.
    def buscar_por_dni(self, dni):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_cliente,
                nombre,
                apellido,
                dni,
                correo,
                telefono,
                fecha_registro
            FROM cliente
            WHERE dni = ?
        """, (dni,))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:
            return self.__fila_a_cliente(fila)

        return None

    # busca un cliente por su ID.
    def buscar_por_id(self, id_cliente):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_cliente,
                nombre,
                apellido,
                dni,
                correo,
                telefono,
                fecha_registro
            FROM cliente
            WHERE id_cliente = ?
        """, (id_cliente,))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:
            return self.__fila_a_cliente(fila)

        return None

    # obtiene todos los clientes registrados.
    def obtener_todos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_cliente,
                nombre,
                apellido,
                dni,
                correo,
                telefono,
                fecha_registro
            FROM cliente
            ORDER BY nombre
        """)

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return [
            self.__fila_a_cliente(fila)
            for fila in filas
        ]

    # actualiza los datos de un cliente.
    def actualizar(
        self,
        id_cliente,
        nombre,
        apellido,
        dni,
        correo,
        telefono,
        fecha_registro
    ):
        cliente = self.buscar_por_id(id_cliente)

        if not cliente:
            self.__log.error(
                f"Actualizar fallido: "
                f"Cliente ID={id_cliente} no existe"
            )
            raise ClienteNoEncontradoError(id_cliente)

        cliente_dni = self.buscar_por_dni(dni)

        if cliente_dni and cliente_dni.id != id_cliente:
            self.__log.warning(
                f"DNI duplicado: {dni}"
            )
            raise DNIDuplicadoError(dni)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE cliente
            SET
                nombre = ?,
                apellido = ?,
                dni = ?,
                correo = ?,
                telefono = ?,
                fecha_registro = ?
            WHERE id_cliente = ?
        """, (
            nombre,
            apellido,
            dni,
            correo,
            telefono,
            fecha_registro,
            id_cliente
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        cliente.nombre = nombre
        cliente.apellido = apellido
        cliente.dni = dni
        cliente.correo = correo
        cliente.telefono = telefono
        cliente.fecha_registro = fecha_registro

        self.__log.info(
            f"Cliente actualizado: ID={id_cliente}"
        )

        return cliente

    # elimina un cliente por su ID.
    def eliminar(self, id_cliente):
        cliente = self.buscar_por_id(id_cliente)

        if not cliente:
            self.__log.error(
                f"Eliminar fallido: "
                f"Cliente ID={id_cliente} no existe"
            )
            raise ClienteNoEncontradoError(id_cliente)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                DELETE FROM cliente
                WHERE id_cliente = ?
            """, (id_cliente,))

            conexion.commit()
        except sqlite3.IntegrityError:
            conexion.rollback()

            self.__log.warning(
                f"Eliminar fallido: "
                f"Cliente ID={id_cliente} "
                f"tiene ventas registradas"
            )

            raise ClienteConVentasError(id_cliente)
        finally:
            cursor.close()
            conexion.close()

        self.__log.info(
            f"Cliente eliminado: "
            f"{cliente.nombre} {cliente.apellido} "
            f"(ID={id_cliente})"
        )

        return True

    # cuenta la cantidad de clientes registrados.
    def total(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM cliente
        """)

        total_clientes = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return total_clientes

    # convierte una fila de SQLite en un objeto Cliente.
    def __fila_a_cliente(self, fila):
        cliente = Cliente(
            fila["nombre"],
            fila["apellido"],
            fila["dni"],
            fila["correo"],
            fila["telefono"],
            fila["fecha_registro"]
        )
        cliente.id = fila["id_cliente"]
        return cliente