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

        return sorted(
            self.__bd,
            key=lambda o: o.nombre_oferta
        )

    # Actualiza una oferta
    def actualizar(
        self,
        id,
        nombre_oferta=None,
        descuento=None,
        fecha_inicio=None,
        fecha_fin=None,
        activa=None
    ):

        oferta = self.buscar_por_id(id)

        if not oferta:

            self.__log.error(
                f"Actualizar fallido: Oferta ID={id} no existe"
            )

            raise OfertaNoEncontradaError(id)

        if nombre_oferta:
            oferta.nombre_oferta = nombre_oferta

        if descuento is not None:
            oferta.descuento = descuento

        if fecha_inicio:
            oferta.fecha_inicio = fecha_inicio

        if fecha_fin:
            oferta.fecha_fin = fecha_fin

        if activa is not None:
            oferta.activa = activa

        self.__log.info(
            f"Oferta actualizada: ID={id}"
        )

        return oferta

    # Elimina una oferta
    def eliminar(self, id):

        oferta = self.buscar_por_id(id)

        if not oferta:

            self.__log.error(
                f"Eliminar fallido: Oferta ID={id} no existe"
            )

            raise OfertaNoEncontradaError(id)

        self.__bd.remove(oferta)

        self.__log.warning(
            f"Oferta eliminada: ID={id}"
        )