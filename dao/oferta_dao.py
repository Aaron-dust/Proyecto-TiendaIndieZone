# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de ofertas del sistema.
# ----------------------------------------------------------------------------------
from config.logger import Logger
from config.base_datos import obtener_conexion
import sqlite3
from modelos.oferta import Oferta

class OfertaNoEncontradaError(Exception):
    def __init__(self, oferta_id):
        super().__init__(f"Oferta ID={oferta_id} no encontrada")


class OfertaDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(f"La oferta '{nombre}' ya existe")


# Se produce cuando una oferta está asociada a uno o más productos.
class OfertaConProductosError(Exception):
    def __init__(self, oferta_id):
        super().__init__(
            f"Oferta ID={oferta_id} no se puede eliminar: tiene productos asociados"
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
        if self.buscar_por_nombre(oferta.nombre_oferta):
            self._log.warning(
                f"Oferta duplicada: {oferta.nombre_oferta}"
            )
            raise OfertaDuplicadaError(oferta.nombre_oferta)
        conn = obtener_conexion()
        cursor = conn.cursor()
        # Inserta una nueva oferta utilizando parámetros seguros.
        cursor.execute(

            """
            INSERT INTO Oferta
            (
                nombre_oferta,
                descuento,
                fecha_inicio,
                fecha_fin,
                activa

            )
            VALUES
            (
                ?, ?, ?, ?, ?
            )
            """,

            (
                oferta.nombre_oferta,
                oferta.descuento,
                oferta.fecha_inicio,
                oferta.fecha_fin,
                oferta.activa
            )

        )
        conn.commit()
        # Guarda el identificador generado automáticamente.
        oferta.id = cursor.lastrowid
        conn.close()
        self._log.info(
            f"Oferta agregada: {oferta.nombre_oferta} (ID={oferta.id})"
        )
        return oferta

    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(

            """
            SELECT *
            FROM Oferta
            WHERE nombre_oferta = ?
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
            FROM Oferta
            WHERE id_oferta = ?
            """,

            (oferta_id,)

        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_oferta(fila) if fila else None
    # Devuelve todas las ofertas
    def obtener_todos(self):

        conn = obtener_conexion()
        cursor = conn.cursor()
        # SQLite realiza el ordenamiento de los registros.
        cursor.execute("""
            SELECT *
            FROM Oferta
            ORDER BY nombre_oferta
        """)

        filas = cursor.fetchall()
        conn.close()
        # Convierte cada fila de la BD en un objeto Oferta.
        return [self._fila_a_oferta(f) for f in filas]

    def actualizar(
        self,
        oferta_id,
        nombre_oferta=None,
        descuento=None,
        fecha_inicio=None,
        fecha_fin=None,
        activa=None
    ):

        o = self.buscar_por_id(oferta_id)
        if not o:
            self._log.error(
                f"Actualizar fallido: Oferta ID={oferta_id} no existe"
            )
            raise OfertaNoEncontradaError(oferta_id)

        # Conserva el valor actual cuando no se envía uno nuevo.
        nuevo_nombre = (
            nombre_oferta
            if nombre_oferta is not None
            else o.nombre_oferta
        )

        nuevo_descuento = (
            descuento
            if descuento is not None
            else o.descuento
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

        nueva_activa = (
            activa
            if activa is not None
            else o.activa
        )

        # Verifica que el nombre no pertenezca a otra oferta.
        oferta_nombre = self.buscar_por_nombre(nuevo_nombre)
        if oferta_nombre and oferta_nombre.id != oferta_id:
            self._log.warning(f"Oferta duplicada: {nuevo_nombre}")
            raise OfertaDuplicadaError(nuevo_nombre)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(

            """
            UPDATE Oferta
            SET
                nombre_oferta = ?,
                descuento = ?,
                fecha_inicio = ?,
                fecha_fin = ?,
                activa = ?

            WHERE id_oferta = ?

            """,
            (
                nuevo_nombre,
                nuevo_descuento,
                nueva_fecha_inicio,
                nueva_fecha_fin,
                nueva_activa,
                oferta_id
            )

        )

        conn.commit()

        conn.close()

        o.nombre_oferta = nuevo_nombre
        o.descuento = nuevo_descuento
        o.fecha_inicio = nueva_fecha_inicio
        o.fecha_fin = nueva_fecha_fin
        o.activa = nueva_activa

        self._log.info(f"Oferta actualizada: ID={oferta_id}")

        return o

    def eliminar(self, oferta_id):

        o = self.buscar_por_id(oferta_id)
        if not o:
            self._log.error(
                f"Eliminar fallido: Oferta ID={oferta_id} no existe"
            )
            raise OfertaNoEncontradaError(oferta_id)

        conn = obtener_conexion()

        cursor = conn.cursor()

        try:

            # No permite eliminar ofertas asociadas a productos.
            cursor.execute(
                """

                DELETE FROM Oferta
                WHERE id_oferta = ?
                """,

                (oferta_id,)

            )

            conn.commit()
            conn.close()
            self._log.info(f"Oferta eliminada: ID={oferta_id}")

        except sqlite3.IntegrityError:

            conn.close()
            self._log.warning(
                f"Eliminar fallido: Oferta ID={oferta_id} tiene productos asociados"
            )
            raise OfertaConProductosError(oferta_id)

    def total(self):

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(

            """
            SELECT COUNT(*)
            FROM Oferta
            """
        )

        total = cursor.fetchone()[0]
        conn.close()
        return total

    def _fila_a_oferta(self, fila):

        # Convierte una fila de SQLite en un objeto Oferta.
        o = Oferta(

            fila["nombre_oferta"],
            fila["descuento"],
            fila["fecha_inicio"],
            fila["fecha_fin"],
            fila["activa"]
        )

        o.id = fila["id_oferta"]
        return o