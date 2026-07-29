import sqlite3

NOMBRE_BD = "indiezone.db"

# abre o crea la base de datos.
def obtener_conexion():
    conexion = sqlite3.connect(NOMBRE_BD)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

# crea las tablas si todavía no existen.
def inicializar():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            dni TEXT UNIQUE NOT NULL,
            correo TEXT,
            telefono TEXT,
            fecha_registro TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_categoria TEXT NOT NULL,
            descripcion TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS oferta (
            id_oferta INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_oferta TEXT NOT NULL,
            descuento REAL NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL,
            activa INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_producto TEXT NOT NULL,
            tipo_producto TEXT NOT NULL,
            descripcion_producto TEXT,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            id_oferta INTEGER,
            FOREIGN KEY (id_categoria)
                REFERENCES categoria(id_categoria),
            FOREIGN KEY (id_oferta)
                REFERENCES oferta(id_oferta)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_venta TEXT NOT NULL,
            total_venta REAL NOT NULL,
            id_cliente INTEGER NOT NULL,
            FOREIGN KEY (id_cliente)
                REFERENCES cliente(id_cliente)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            PRIMARY KEY (
                id_venta,
                id_producto
            ),
            FOREIGN KEY (id_venta)
                REFERENCES venta(id_venta),
            FOREIGN KEY (id_producto)
                REFERENCES producto(id_producto)
        )
    """)

    conexion.commit()
    conexion.close()