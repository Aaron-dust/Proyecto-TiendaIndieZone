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