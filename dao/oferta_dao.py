# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de ofertas del sistema.
# ----------------------------------------------------------------------------------

from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.oferta import Oferta
import psycopg2

class OfertaNoEncontradaError(Exception):
    def __init__(self, oferta_id):
        super().__init__(
            f"Oferta ID={oferta_id} no encontrada"
        )

class OfertaDuplicadaError(Exception):

    def __init__(self, nombre):
        super().__init__(
            f"La oferta '{nombre}' ya existe"
        )

class OfertaConProductosError(Exception):
    def __init__(self, oferta_id):
        super().__init__(
            f"Oferta ID={oferta_id} no se puede eliminar: "
            f"tiene productos asociados"
        )

class OfertaDAO:
    def __init__(self):
        self._log = Logger()
    def insertar(self, oferta):

        # Verifica si ya existe una oferta con el mismo nombre
        if self.buscar_por_nombre(oferta.nombre):
            self._log.warning(
                f"Oferta duplicada: {oferta.nombre}"
            )
            raise OfertaDuplicadaError(
                oferta.nombre
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
            VALUES
            (
                %s, %s, %s, %s
            )
            RETURNING id_oferta
            """,
            (
                oferta.nombre,
                oferta.porcentaje_descuento,
                oferta.fecha_inicio,
                oferta.fecha_fin
            )
        )
        fila = cursor.fetchone()
        oferta.id_oferta = fila["id_oferta"]
        conn.commit()
        cursor.close()
        conn.close()
        self._log.info(
            f"Oferta agregada: {oferta.nombre} "
            f"(ID={oferta.id_oferta})"
        )
        return oferta

    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM oferta
            WHERE nombre = %s
            """,
            (nombre,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return self._fila_a_oferta(fila) if fila else None

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
        return self._fila_a_oferta(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM oferta
            ORDER BY nombre
            """
        )
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_oferta(fila)
            for fila in filas
        ]

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
            raise OfertaNoEncontradaError(oferta_id)
        nuevo_nombre = (
            nombre
            if nombre is not None
            else oferta.nombre
        )
        nuevo_porcentaje = (
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

        # Comprueba que el nombre no pertenezca a otra oferta
        otra_oferta = self.buscar_por_nombre(
            nuevo_nombre
        )
        if (
            otra_oferta
            and otra_oferta.id_oferta != oferta_id
        ):
            raise OfertaDuplicadaError(
                nuevo_nombre
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
                nuevo_porcentaje,
                nueva_fecha_inicio,
                nueva_fecha_fin,
                oferta_id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        oferta.nombre = nuevo_nombre
        oferta.porcentaje_descuento = nuevo_porcentaje
        oferta.fecha_inicio = nueva_fecha_inicio
        oferta.fecha_fin = nueva_fecha_fin

        self._log.info(
            f"Oferta actualizada: ID={oferta_id}"
        )
        return oferta

    def eliminar(self, oferta_id):
        oferta = self.buscar_por_id(oferta_id)
        if not oferta:
            raise OfertaNoEncontradaError(oferta_id)
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
            self._log.info(
                f"Oferta eliminada: ID={oferta_id}"
            )
        except psycopg2.IntegrityError:
            conn.rollback()

            raise OfertaConProductosError(
                oferta_id
            )
        finally:
            cursor.close()
            conn.close()

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM oferta
            """
        )
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total

    def _fila_a_oferta(self, fila):
        oferta = Oferta(
            fila["nombre"],
            fila["porcentaje_descuento"],
            fila["fecha_inicio"],
            fila["fecha_fin"]
        )
        oferta.id_oferta = fila["id_oferta"]
        return oferta
