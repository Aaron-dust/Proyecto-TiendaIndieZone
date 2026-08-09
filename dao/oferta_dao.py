# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de ofertas del sistema.
# ----------------------------------------------------------------------------------
from config.logger import Logger
from config.base_datos import obtener_conexion
import psycopg2
from modelos.oferta import Oferta

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
# Se produce cuando una oferta está asociada a uno o más productos.
class OfertaConProductosError(Exception):

    def __init__(self, oferta_id):
        super().__init__(
            f"Oferta ID={oferta_id} no se puede eliminar: "
            f"tiene productos asociados"
        )
# ----------------------------------------------------------------------------------
# PATRÓN DAO – OfertaDAO
#
# Encapsula todas las operaciones relacionadas con la tabla Oferta.
# ----------------------------------------------------------------------------------

class OfertaDAO:
    def __init__(self):
        self._log = Logger()
    def insertar(self, oferta):
        # Verifica que la oferta no exista previamente.
        if self.buscar_por_nombre(oferta.nombre):
            self._log.warning(
                f"Oferta duplicada: {oferta.nombre}"
            )
            raise OfertaDuplicadaError(
                oferta.nombre
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        # Inserta una nueva oferta utilizando parámetros seguros.
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
        # Guarda el identificador generado automáticamente.
        oferta.id = cursor.fetchone()["id_oferta"]
        conn.commit()
        conn.close()
        self._log.info(
            f"Oferta agregada: {oferta.nombre} "
            f"(ID={oferta.id})"
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
        conn.close()
        return self._fila_a_oferta(fila) if fila else None
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # PostgreSQL realiza el ordenamiento de los registros.
        cursor.execute(
            """
            SELECT *
            FROM oferta
            ORDER BY nombre
            """
        )
        filas = cursor.fetchall()
        conn.close()
        # Convierte cada fila de la BD en un objeto Oferta.
        return [
            self._fila_a_oferta(f)
            for f in filas
        ]
    def actualizar(
        self,
        oferta_id,
        nombre=None,
        porcentaje_descuento=None,
        fecha_inicio=None,
        fecha_fin=None
    ):
        o = self.buscar_por_id(oferta_id)
        if not o:
            self._log.error(
                f"Actualizar fallido: Oferta ID={oferta_id} "
                f"no existe"
            )
            raise OfertaNoEncontradaError(
                oferta_id
            )
        # Conserva el valor actual cuando no se envía uno nuevo.
        nuevo_nombre = (
            nombre
            if nombre is not None
            else o.nombre
        )
        nuevo_porcentaje = (
            porcentaje_descuento
            if porcentaje_descuento is not None
            else o.porcentaje_descuento
        )
        nueva_fecha_inicio = (
            fecha_inicio
            if fecha_inicio is not None
            else o.fecha_inicio
        )
        nueva_fecha_fin = (
            fecha_fin
            if fecha_fin is not None
            else o.fecha_fin
        )
        # Verifica que el nombre no pertenezca a otra oferta.
        oferta_nombre = self.buscar_por_nombre(
            nuevo_nombre
        )
        if oferta_nombre and oferta_nombre.id != oferta_id:
            self._log.warning(
                f"Oferta duplicada: {nuevo_nombre}"
            )
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
        conn.close()
        o.nombre = nuevo_nombre
        o.porcentaje_descuento = nuevo_porcentaje
        o.fecha_inicio = nueva_fecha_inicio
        o.fecha_fin = nueva_fecha_fin
        self._log.info(
            f"Oferta actualizada: ID={oferta_id}"
        )
        return o

    def eliminar(self, oferta_id):
        o = self.buscar_por_id(oferta_id)
        if not o:
            self._log.error(
                f"Eliminar fallido: Oferta ID={oferta_id} "
                f"no existe"
            )
            raise OfertaNoEncontradaError(
                oferta_id
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            # No permite eliminar ofertas asociadas a productos.
            cursor.execute(
                """
                DELETE FROM oferta
                WHERE id_oferta = %s
                """,
                (oferta_id,)
            )
            conn.commit()
            conn.close()
            self._log.info(
                f"Oferta eliminada: ID={oferta_id}"
            )
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            self._log.warning(
                f"Eliminar fallido: Oferta ID={oferta_id} "
                f"tiene productos asociados"
            )
            raise OfertaConProductosError(
                oferta_id
            )

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
        conn.close()
        return total
    def _fila_a_oferta(self, fila):
        # Convierte una fila de PostgreSQL en un objeto Oferta.
        o = Oferta(
            fila["nombre"],
            fila["porcentaje_descuento"],
            fila["fecha_inicio"],
            fila["fecha_fin"]
        )
        o.id = fila["id_oferta"]
        return o