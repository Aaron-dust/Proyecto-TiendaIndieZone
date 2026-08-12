# dao/oferta_dao.py

import psycopg2

from config.base_datos import obtener_conexion
from modelos.oferta import Oferta

class OfertaNoEncontradaError(Exception):
    pass

class OfertaDuplicadaError(Exception):
    pass

class OfertaConProductosError(Exception):
    pass

class OfertaDAO:
    # Busca una oferta por su ID.
    def buscar_por_id(self, oferta_id):
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM oferta
            WHERE id_oferta = %s
            """,
            (oferta_id,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_oferta(fila)

    # Busca una oferta por nombre.
    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM oferta
            WHERE LOWER(nombre) = LOWER(%s)
            """,
            (nombre,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_oferta(fila)

    # Devuelve todas las ofertas.
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM oferta
            ORDER BY id_oferta
            """
        )
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_oferta(fila)
            for fila in filas
        ]

    # Inserta una nueva oferta.
    def insertar(self, oferta):
        if self.buscar_por_nombre(oferta.nombre):
            raise OfertaDuplicadaError(
                "La oferta ya existe"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO oferta
            (
                nombre,
                porcentaje_descuento,
                fecha_inicio,
                fecha_fin
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id_oferta
            """,
            (
                oferta.nombre,
                oferta.porcentaje_descuento,
                oferta.fecha_inicio,
                oferta.fecha_fin
            )
        )
        oferta.id = cursor.fetchone()["id_oferta"]
        conn.commit()
        cursor.close()
        conn.close()
        return oferta

    # Actualiza una oferta.
    def actualizar(
        self,
        oferta_id,
        nombre=None,
        porcentaje_descuento=None,
        fecha_inicio=None,
        fecha_fin=None
    ):
        oferta = self.buscar_por_id(oferta_id)
        if not oferta:
            raise OfertaNoEncontradaError(
                "Oferta no encontrada"
            )
        nuevo_nombre = (
            nombre
            if nombre is not None
            else oferta.nombre
        )
        nuevo_descuento = (
            porcentaje_descuento
            if porcentaje_descuento is not None
            else oferta.porcentaje_descuento
        )
        nueva_fecha_inicio = (
            fecha_inicio
            if fecha_inicio is not None
            else oferta.fecha_inicio
        )
        nueva_fecha_fin = (
            fecha_fin
            if fecha_fin is not None
            else oferta.fecha_fin
        )
        otra_oferta = self.buscar_por_nombre(
            nuevo_nombre
        )
        if (
            otra_oferta
            and otra_oferta.id != oferta_id
        ):
            raise OfertaDuplicadaError(
                "Ya existe otra oferta con ese nombre"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE oferta
            SET
                nombre = %s,
                porcentaje_descuento = %s,
                fecha_inicio = %s,
                fecha_fin = %s
            WHERE id_oferta = %s
            """,
            (
                nuevo_nombre,
                nuevo_descuento,
                nueva_fecha_inicio,
                nueva_fecha_fin,
                oferta_id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return self.buscar_por_id(oferta_id)

    # Elimina una oferta si no está siendo usada.
    def eliminar(self, oferta_id):
        if not self.buscar_por_id(oferta_id):
            raise OfertaNoEncontradaError(
                "Oferta no encontrada"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM oferta
                WHERE id_oferta = %s
                """,
                (oferta_id,)
            )
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            raise OfertaConProductosError(
                "La oferta tiene productos asociados"
            )
        finally:
            cursor.close()
            conn.close()

    # Convierte una fila de PostgreSQL en un objeto Oferta.
    def _fila_a_oferta(self, fila):
        oferta = Oferta(
            fila["nombre"],
            fila["porcentaje_descuento"],
            fila["fecha_inicio"],
            fila["fecha_fin"]
        )
        oferta.id = fila["id_oferta"]
        return oferta
