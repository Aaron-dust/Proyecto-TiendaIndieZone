# dao/venta_dao.py

from config.base_datos import obtener_conexion
from modelos.venta import Venta

class VentaNoEncontradaError(Exception):
    pass

class VentaDAO:
    def insertar(self, venta):
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO venta
            (
                fecha_venta,
                total_venta,
                id_cliente
            )
            VALUES (%s, %s, %s)
            RETURNING id_venta
        """, (
            venta.fecha_venta,
            venta.total_venta,
            venta.id_cliente
        ))
        venta.id = (
            cursor.fetchone()["id_venta"]
        )
        conn.commit()
        cursor.close()
        conn.close()
        return venta

    def buscar_por_id(self, venta_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM venta
            WHERE id_venta = %s
        """, (venta_id,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_venta(fila)

    def buscar_por_cliente(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM venta
            WHERE id_cliente = %s
            ORDER BY fecha_venta DESC
        """, (cliente_id,))
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_venta(fila)
            for fila in filas
        ]

    def resumen_por_cliente(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) AS cantidad_ventas,
                COALESCE(
                    SUM(total_venta),
                    0
                ) AS total_comprado
            FROM venta
            WHERE id_cliente = %s
        """, (cliente_id,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "cantidad_ventas":
                fila["cantidad_ventas"],
            "total_comprado":
                float(fila["total_comprado"])
        }

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM venta
            ORDER BY fecha_venta DESC
        """)
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_venta(fila)
            for fila in filas
        ]

    def _fila_a_venta(self, fila):
        venta = Venta(
            fila["fecha_venta"],
            fila["total_venta"],
            fila["id_cliente"]
        )
        venta.id = fila["id_venta"]
        return venta
