import sqlite3
from config.base_datos import obtener_conexion
from config.logger import Logger
from modelos.oferta import Oferta

class OfertaNoEncontradaError(Exception):

    # crea el mensaje para una oferta inexistente.
    def __init__(self, id_oferta):
        super().__init__(
            f"No existe una oferta con ID={id_oferta}"
        )

class OfertaConProductosError(Exception):

    # crea el mensaje cuando la oferta tiene productos.
    def __init__(self, id_oferta):
        super().__init__(
            f"No se puede eliminar la oferta ID={id_oferta} "
            f"porque tiene productos registrados"
        )

class OfertaDAO:

    # utiliza el historial compartido del sistema.
    def __init__(self):
        self.__log = Logger()

    # inserta una oferta en la base de datos.
    def insertar(self, oferta):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO oferta
            (
                nombre_oferta,
                descuento,
                fecha_inicio,
                fecha_fin,
                activa
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """, (
            oferta.nombre,
            oferta.descuento,
            oferta.fecha_inicio,
            oferta.fecha_fin,
            oferta.activa
        ))

        conexion.commit()
        oferta.id = cursor.lastrowid

        cursor.close()
        conexion.close()

        self.__log.info(
            f"Oferta agregada: {oferta.nombre} "
            f"(ID={oferta.id})"
        )

        return oferta

    # busca una oferta por su ID.
    def buscar_por_id(self, id_oferta):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_oferta,
                nombre_oferta,
                descuento,
                fecha_inicio,
                fecha_fin,
                activa
            FROM oferta
            WHERE id_oferta = ?
        """, (id_oferta,))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:
            return self.__fila_a_oferta(fila)

        return None

    # obtiene todas las ofertas registradas.
    def obtener_todos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_oferta,
                nombre_oferta,
                descuento,
                fecha_inicio,
                fecha_fin,
                activa
            FROM oferta
            ORDER BY nombre_oferta
        """)

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return [
            self.__fila_a_oferta(fila)
            for fila in filas
        ]

    # actualiza los datos de una oferta.
    def actualizar(
        self,
        id_oferta,
        nombre,
        descuento,
        fecha_inicio,
        fecha_fin,
        activa
    ):
        oferta = self.buscar_por_id(id_oferta)

        if not oferta:
            self.__log.error(
                f"Actualizar fallido: "
                f"Oferta ID={id_oferta} no existe"
            )
            raise OfertaNoEncontradaError(id_oferta)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE oferta
            SET
                nombre_oferta = ?,
                descuento = ?,
                fecha_inicio = ?,
                fecha_fin = ?,
                activa = ?
            WHERE id_oferta = ?
        """, (
            nombre,
            descuento,
            fecha_inicio,
            fecha_fin,
            activa,
            id_oferta
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        oferta.nombre = nombre
        oferta.descuento = descuento
        oferta.fecha_inicio = fecha_inicio
        oferta.fecha_fin = fecha_fin
        oferta.activa = activa

        self.__log.info(
            f"Oferta actualizada: ID={id_oferta}"
        )

        return oferta

    # elimina una oferta por su ID.
    def eliminar(self, id_oferta):
        oferta = self.buscar_por_id(id_oferta)

        if not oferta:
            self.__log.error(
                f"Eliminar fallido: "
                f"Oferta ID={id_oferta} no existe"
            )
            raise OfertaNoEncontradaError(id_oferta)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                DELETE FROM oferta
                WHERE id_oferta = ?
            """, (id_oferta,))

            conexion.commit()
        except sqlite3.IntegrityError:
            conexion.rollback()

            self.__log.warning(
                f"Eliminar fallido: "
                f"Oferta ID={id_oferta} "
                f"tiene productos registrados"
            )

            raise OfertaConProductosError(id_oferta)
        finally:
            cursor.close()
            conexion.close()

        self.__log.info(
            f"Oferta eliminada: {oferta.nombre} "
            f"(ID={id_oferta})"
        )

        return True

    # cuenta la cantidad de ofertas registradas.
    def total(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM oferta
        """)

        total_ofertas = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return total_ofertas

    # convierte una fila de SQLite en un objeto Oferta.
    def __fila_a_oferta(self, fila):
        oferta = Oferta(
            fila["nombre_oferta"],
            fila["descuento"],
            fila["fecha_inicio"],
            fila["fecha_fin"],
            bool(fila["activa"])
        )
        oferta.id = fila["id_oferta"]
        return oferta