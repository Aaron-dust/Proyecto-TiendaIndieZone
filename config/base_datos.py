import sqlite3

# Archivo donde SQLite almacenará toda la información del sistema.
ARCHIVO_BD = "TiendaIndieZone.db"

def obtener_conexion():
    # Abre la conexión con la base de datos o la crea si no existe.
    conn = sqlite3.connect(ARCHIVO_BD)
    # Activa las restricciones de claves foráneas.
    conn.execute("PRAGMA foreign_keys = ON")
    # Permite acceder a los registros mediante el nombre de la columna.
    conn.row_factory = sqlite3.Row
    return conn


def inicializar():
    # Crea las tablas la primera vez que se ejecuta el sistema.
    conn = obtener_conexion()
    cursor = conn.cursor()

    # ==========================
    # TABLA CLIENTE
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cliente(

            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL,

            apellido TEXT NOT NULL,

            dni TEXT UNIQUE NOT NULL,

            correo TEXT UNIQUE NOT NULL,

            telefono TEXT NOT NULL,

            fecha_registro TEXT NOT NULL

        )
    """)
    # ==========================
    # TABLA CATEGORIA
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categoria(

            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre_categoria TEXT NOT NULL,

            descripcion TEXT

        )
    """)
    # ==========================
    # TABLA OFERTA
    # ==========================
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
    # ==========================
    # TABLA PRODUCTO
    # ==========================
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
    # ==========================
    # TABLA VENTA
    # ==========================
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
    # ==========================
    # TABLA DETALLE_VENTA
    # ==========================
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
    # Guarda los cambios realizados.
    conn.commit()
    conn.close()