# dao/cliente_dao.py

import psycopg2

from config.base_datos import obtener_conexion
from modelos.cliente import Cliente

class ClienteNoEncontradoError(Exception):
    pass

class DNIDuplicadoError(Exception):
    pass

class ClienteConVentasError(Exception):
    pass

class ClienteDAO:
    def insertar(self, cliente):
        if self.buscar_por_dni(cliente.dni):
            raise DNIDuplicadoError(
                f"El DNI {cliente.dni} ya existe"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
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
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_cliente
        """, (
            cliente.nombre,
            cliente.apellido,
            cliente.dni,
            cliente.correo,
            cliente.telefono,
            cliente.fecha_registro
        ))
        cliente.id = cursor.fetchone()["id_cliente"]
        conn.commit()
        cursor.close()
        conn.close()
        return cliente

    def buscar_por_id(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM cliente
            WHERE id_cliente = %s
        """, (cliente_id,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None

        return self._fila_a_cliente(fila)

    def buscar_por_dni(self, dni):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM cliente
            WHERE dni = %s
        """, (dni,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_cliente(fila)

    def buscar(
        self,
        dni=None,
        nombre=None,
        correo=None
    ):
        conn = obtener_conexion()
        cursor = conn.cursor()

        consulta = """
            SELECT *
            FROM cliente
            WHERE 1 = 1
        """
        parametros = []
        if dni:
            consulta += " AND dni ILIKE %s"
            parametros.append(f"%{dni}%")
        if nombre:
            consulta += """
                AND (
                    nombre ILIKE %s
                    OR apellido ILIKE %s
                    OR CONCAT(nombre, ' ', apellido) ILIKE %s
                )
            """
            texto = f"%{nombre}%"
            parametros.extend([
                texto,
                texto,
                texto
            ])
        if correo:
            consulta += " AND correo ILIKE %s"
            parametros.append(f"%{correo}%")
        consulta += " ORDER BY nombre, apellido"
        cursor.execute(
            consulta,
            tuple(parametros)
        )
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_cliente(fila)
            for fila in filas
        ]

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM cliente
            ORDER BY nombre, apellido
        """)

        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_cliente(fila)
            for fila in filas
        ]

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
        cliente = self.buscar_por_id(cliente_id)
        if not cliente:
            raise ClienteNoEncontradoError(
                f"Cliente ID={cliente_id} no encontrado"
            )
        nuevo_nombre = nombre or cliente.nombre
        nuevo_apellido = apellido or cliente.apellido
        nuevo_dni = dni or cliente.dni
        nuevo_correo = correo or cliente.correo
        nuevo_telefono = telefono or cliente.telefono
        nueva_fecha = (
            fecha_registro
            if fecha_registro is not None
            else cliente.fecha_registro
        )
        cliente_dni = self.buscar_por_dni(nuevo_dni)
        if (
            cliente_dni
            and cliente_dni.id != cliente_id
        ):
            raise DNIDuplicadoError(
                f"El DNI {nuevo_dni} ya existe"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE cliente
            SET
                nombre = %s,
                apellido = %s,
                dni = %s,
                correo = %s,
                telefono = %s,
                fecha_registro = %s
            WHERE id_cliente = %s
        """, (
            nuevo_nombre,
            nuevo_apellido,
            nuevo_dni,
            nuevo_correo,
            nuevo_telefono,
            nueva_fecha,
            cliente_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return self.buscar_por_id(cliente_id)

    def eliminar(self, cliente_id):
        if not self.buscar_por_id(cliente_id):
            raise ClienteNoEncontradoError(
                f"Cliente ID={cliente_id} no encontrado"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM cliente
                WHERE id_cliente = %s
            """, (cliente_id,))

            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()

            raise ClienteConVentasError(
                "El cliente tiene ventas registradas"
            )
        finally:
            cursor.close()
            conn.close()

    def _fila_a_cliente(self, fila):
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
