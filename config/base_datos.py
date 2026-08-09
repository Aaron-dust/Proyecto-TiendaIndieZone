import os
import psycopg2
from psycopg2.extras import RealDictCursor


def obtener_conexion():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "tiendaindiezone"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "admin123")
    )

    conn.cursor_factory = RealDictCursor
    return conn


def inicializar():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            dni VARCHAR(8) UNIQUE NOT NULL,
            correo VARCHAR(100) NOT NULL,
            telefono VARCHAR(15) NOT NULL,
            fecha_registro DATE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            descripcion VARCHAR(150)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS oferta (
            id_oferta SERIAL PRIMARY KEY,
            nombre VARCHAR(80) NOT NULL,
            porcentaje_descuento NUMERIC(5,2) NOT NULL,
            fecha_inicio DATE NOT NULL,
            fecha_fin DATE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            id_producto SERIAL PRIMARY KEY,
            nombre_producto VARCHAR(100) NOT NULL,
            tipo_producto VARCHAR(30) NOT NULL,
            descripcion_producto VARCHAR(200),
            precio NUMERIC(10,2) NOT NULL,
            stock INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            id_oferta INTEGER,
            FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
            FOREIGN KEY (id_oferta) REFERENCES oferta(id_oferta)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta (
            id_venta SERIAL PRIMARY KEY,
            fecha_venta DATE NOT NULL,
            total_venta NUMERIC(10,2) NOT NULL,
            id_cliente INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario NUMERIC(10,2) NOT NULL,
            subtotal NUMERIC(10,2) NOT NULL,
            PRIMARY KEY (id_venta, id_producto),
            FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )
    """)

    conn.commit()
    conn.close()