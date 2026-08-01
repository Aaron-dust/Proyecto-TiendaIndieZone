    def obtener_todos(self):

        conn = obtener_conexion()

        cursor = conn.cursor()

        # SQLite realiza el ordenamiento por id de venta.
        cursor.execute("""

            SELECT *

            FROM Detalle_Venta

            ORDER BY id_venta

        """)

        filas = cursor.fetchall()

        conn.close()

        # Convierte cada fila de la BD en un objeto DetalleVenta.
        return [self._fila_a_detalle(f) for f in filas]

    def actualizar(
        self,
        id_venta,
        id_producto,
        cantidad=None,
        precio_unitario=None,
        subtotal=None
    ):

        d = self.buscar(id_venta, id_producto)

        if not d:

            self._log.error(

                f"Actualizar fallido: Venta={id_venta} Producto={id_producto}"

            )

            raise DetalleVentaNoEncontradoError(
                id_venta,
                id_producto
            )

        # Conserva los valores actuales cuando no se envían nuevos.
        nueva_cantidad = (
            cantidad
            if cantidad is not None
            else d.cantidad
        )

        nuevo_precio = (
            precio_unitario
            if precio_unitario is not None
            else d.precio_unitario
        )

        nuevo_subtotal = (
            subtotal
            if subtotal is not None
            else d.subtotal
        )

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(

            """

            UPDATE Detalle_Venta

            SET

                cantidad = ?,

                precio_unitario = ?,

                subtotal = ?

            WHERE id_venta = ?

            AND id_producto = ?

            """,

            (

                nueva_cantidad,
                nuevo_precio,
                nuevo_subtotal,
                id_venta,
                id_producto

            )

        )