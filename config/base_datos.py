import sqlite3


class BaseDatos:
    """Administra la conexión con SQLite."""

    def __init__(self):

        # Nombre del archivo de la base de datos
        self.__nombre_bd = "TiendaIndieZone.db"

        self.__conexion = None

    # Abre la conexión
    def conectar(self):

        self.__conexion = sqlite3.connect(self.__nombre_bd)

        return self.__conexion

    # Cierra la conexión
    def cerrar(self):

        if self.__conexion:

            self.__conexion.close()

    # Crea las tablas del sistema
    def crear_tablas(self):

        conexion = self.conectar()

        cursor = conexion.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS Cliente(

            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL,

            apellido TEXT NOT NULL,

            correo TEXT NOT NULL UNIQUE,

            telefono TEXT NOT NULL,

            fecha_registro TEXT NOT NULL

        )

        """)

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS Categoria(

            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre_categoria TEXT NOT NULL,

            descripcion TEXT

        )

        """)
        cursor.execute("""

        CREATE TABLE IF NOT EXISTS Oferta(

            id_oferta INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre_oferta TEXT NOT NULL,

            descuento REAL NOT NULL,

            fecha_inicio TEXT NOT NULL,

            fecha_fin TEXT NOT NULL,

            activa INTEGER NOT NULL

        )

        """)

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS Producto(

            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre_producto TEXT NOT NULL,

            tipo_producto TEXT NOT NULL,

            descripcion_producto TEXT,

            precio REAL NOT NULL,

            stock INTEGER NOT NULL,

            id_categoria INTEGER NOT NULL,

            id_oferta INTEGER,

            FOREIGN KEY(id_categoria)

                REFERENCES Categoria(id_categoria),

            FOREIGN KEY(id_oferta)

                REFERENCES Oferta(id_oferta)

        )

        """)

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS Venta(

            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,

            fecha_venta TEXT NOT NULL,

            total_venta REAL NOT NULL,

            id_cliente INTEGER NOT NULL,

            FOREIGN KEY(id_cliente)

                REFERENCES Cliente(id_cliente)

        )

        """)

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS Detalle_Venta(

            id_venta INTEGER NOT NULL,

            id_producto INTEGER NOT NULL,

            cantidad INTEGER NOT NULL,

            precio_unitario REAL NOT NULL,

            subtotal REAL NOT NULL,

            PRIMARY KEY(id_venta,id_producto),

            FOREIGN KEY(id_venta)

                REFERENCES Venta(id_venta),

            FOREIGN KEY(id_producto)

                REFERENCES Producto(id_producto)

        )

        """)

        conexion.commit()

        self.cerrar()