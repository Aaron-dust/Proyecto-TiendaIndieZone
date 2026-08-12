# TiendaIndieZone — Backend

## 1. Descripción del proyecto

**TiendaIndieZone** es un sistema de gestión para una tienda de videojuegos y consolas, desarrollado bajo una arquitectura de API REST.

El backend permite gestionar clientes, categorías, ofertas, productos y ventas mediante endpoints HTTP. La aplicación utiliza **FastAPI** como framework para la construcción de la API y **PostgreSQL** como sistema gestor de base de datos.

La aplicación se ejecuta mediante **Uvicorn** y proporciona documentación interactiva mediante Swagger UI.

---

## 2. Tecnologías utilizadas

| Tecnología | Uso                                      |
| ---------- | ---------------------------------------- |
| Python     | Lenguaje principal del backend           |
| FastAPI    | Desarrollo de la API REST                |
| Uvicorn    | Servidor ASGI para ejecutar FastAPI      |
| PostgreSQL | Sistema gestor de base de datos          |
| psycopg2   | Conexión entre Python y PostgreSQL       |
| Pydantic   | Validación y estructuración de datos     |
| SQL        | Consultas y operaciones sobre PostgreSQL |

### Instalación de dependencias

Las principales librerías utilizadas son:

```bash
python -m pip install fastapi
python -m pip install uvicorn
python -m pip install psycopg2-binary
python -m pip install pydantic
```

---

# 3. Arquitectura del backend

El proyecto está organizado utilizando una separación por capas:

```text
                    CLIENTE / FRONTEND
                           │
                           ▼
                      FASTAPI
                           │
                           ▼
                        ROUTERS
                           │
                           ▼
                        SCHEMAS
                           │
                           ▼
                         MODELOS
                           │
                           ▼
                           DAO
                           │
                           ▼
                        psycopg2
                           │
                           ▼
                       POSTGRESQL
```

Cada capa tiene una responsabilidad específica.

### Routers

Reciben las peticiones HTTP y determinan qué operación debe ejecutarse.

### Schemas

Definen la estructura de los datos recibidos y enviados por la API. También permiten realizar validaciones mediante Pydantic.

### Modelos

Representan las entidades utilizadas por el sistema.

### DAO

Se encargan directamente del acceso a la base de datos. Las consultas SQL se encuentran encapsuladas dentro de esta capa.

### PostgreSQL

Almacena permanentemente la información del sistema.

---

# 4. Estructura del proyecto

La estructura general del backend es:

```text
TiendaIndieZone/
│
├── config/
│   ├── base_datos.py
│   ├── logger.py
│   └── sistema_config.py
│
├── dao/
│   ├── cliente_dao.py
│   ├── categoria_dao.py
│   ├── oferta_dao.py
│   ├── producto_dao.py
│   ├── venta_dao.py
│   └── detalle_venta_dao.py
│
├── modelos/
│   ├── cliente.py
│   ├── categoria.py
│   ├── oferta.py
│   ├── producto.py
│   ├── venta.py
│   └── detalle_venta.py
│
├── schemas/
│   ├── cliente_schema.py
│   ├── categoria_schema.py
│   ├── oferta_schema.py
│   ├── producto_schema.py
│   ├── venta_schema.py
│   └── detalle_venta_schema.py
│
├── routers/
│   ├── clientes.py
│   ├── categorias.py
│   ├── ofertas.py
│   ├── productos.py
│   ├── ventas.py
│   └── detalle_ventas.py
│
└── main.py
```

El antiguo menú de consola no forma parte de la ejecución de esta versión del proyecto, ya que la interacción se realiza mediante la API REST.

---

# 5. Base de datos PostgreSQL

El backend utiliza **PostgreSQL** como sistema gestor de base de datos.

La conexión se realiza mediante `psycopg2`.

La configuración utiliza parámetros como:

```python
conn = psycopg2.connect(
    host=...,
    port=...,
    database=...,
    user=...,
    password=...
)
```

También se utiliza `RealDictCursor`, permitiendo trabajar con los resultados de las consultas mediante los nombres de las columnas:

```python
fila["nombre"]
fila["id_cliente"]
```

en lugar de acceder a las posiciones numéricas de las columnas.

---

# 6. Tablas principales

La base de datos está organizada alrededor de las siguientes entidades:

```text
CLIENTE
CATEGORIA
OFERTA
PRODUCTO
VENTA
DETALLE_VENTA
```

### Cliente

Almacena la información de los clientes registrados.

Entre sus datos se encuentran:

* ID del cliente
* Nombre
* Apellido
* DNI
* Correo
* Teléfono
* Fecha de registro

### Categoría

Permite clasificar los productos de la tienda.

### Oferta

Almacena las promociones y descuentos disponibles para los productos.

### Producto

Contiene la información de los productos comercializados.

Los productos se relacionan con una categoría y pueden estar asociados a una oferta.

### Venta

Representa la operación de venta realizada a un cliente.

### Detalle_Venta

Permite registrar los productos incluidos dentro de una venta.

La separación entre `VENTA` y `DETALLE_VENTA` permite que una venta pueda contener varios productos.

Ejemplo:

```text
VENTA #1
Cliente: Juan Pérez

DETALLE_VENTA
├── Producto A → cantidad 2
├── Producto B → cantidad 1
└── Producto C → cantidad 3
```

---

# 7. Uso del patrón DAO

El proyecto utiliza el patrón **Data Access Object (DAO)**.

Su objetivo es separar el acceso a la base de datos del resto de la aplicación.

Por ejemplo:

```text
Router
   ↓
DAO
   ↓
PostgreSQL
```

El router no ejecuta directamente las consultas SQL.

En su lugar, solicita una operación al DAO:

```python
dao.obtener_todos()
```

o:

```python
dao.buscar_por_id(id)
```

Esto permite mantener una separación clara entre la lógica de la API y el acceso a los datos.

---

# 8. Operaciones CRUD

Los DAO implementan las operaciones necesarias para gestionar los datos:

### CREATE

Registro de nuevos elementos mediante consultas `INSERT`.

### READ

Consulta de registros mediante `SELECT`.

### UPDATE

Modificación de información mediante `UPDATE`, cuando la entidad permite esta operación.

### DELETE

Eliminación mediante `DELETE`, cuando corresponde según las reglas del sistema.

Las operaciones de venta tienen una consideración especial: las ventas registradas representan operaciones históricas y **no se actualizan ni se eliminan**.

---

# 9. PostgreSQL y consultas parametrizadas

Las consultas utilizan parámetros de PostgreSQL mediante `%s`.

Ejemplo:

```python
cursor.execute(
    "SELECT * FROM cliente WHERE id_cliente = %s",
    (cliente_id,)
)
```

Esto permite separar la consulta SQL de los valores proporcionados por el usuario y evita construir consultas mediante concatenación directa de cadenas.

Para las inserciones también se utilizan parámetros:

```python
cursor.execute(
    """
    INSERT INTO cliente
    (nombre, apellido, dni, correo, telefono, fecha_registro)
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
    (
        cliente.nombre,
        cliente.apellido,
        cliente.dni,
        cliente.correo,
        cliente.telefono,
        cliente.fecha_registro
    )
)
```

---

# 10. Generación de identificadores

PostgreSQL utiliza columnas `SERIAL` para generar automáticamente los identificadores.

Para recuperar el ID generado después de una inserción se utiliza:

```sql
RETURNING
```

Por ejemplo:

```sql
INSERT INTO cliente (...)
VALUES (...)
RETURNING id_cliente
```

Después, Python obtiene el identificador generado mediante:

```python
fila = cursor.fetchone()
```

Esto permite asignar el ID generado al objeto correspondiente.

---

# 11. Schemas con Pydantic

Los schemas permiten definir qué información recibe y devuelve cada endpoint.

Se utilizan diferentes schemas según la operación.

Por ejemplo:

```text
EntidadCrear
EntidadActualizar
EntidadRespuesta
```

Esto permite separar:

* información necesaria para crear;
* información permitida para actualizar;
* información que devuelve la API.

---

# 12. Validadores

Una de las funciones importantes de Pydantic es validar los datos antes de que lleguen a la lógica de acceso a datos.

Por ejemplo, para un DNI se puede comprobar que tenga exactamente 8 dígitos:

```python
@field_validator("dni")
@classmethod
def validar_dni(cls, valor):
    if not re.fullmatch(r"\d{8}", valor):
        raise ValueError(
            "El DNI debe tener exactamente 8 dígitos numéricos"
        )
    return valor
```

De esta manera, si el usuario envía información incorrecta, FastAPI puede rechazarla antes de ejecutar la operación correspondiente en el DAO.

También se pueden realizar validaciones de:

* correo electrónico;
* cantidades;
* precios;
* porcentajes de descuento;
* fechas;
* stock;
* valores obligatorios.

La validación depende de las reglas establecidas para cada entidad.

---

# 13. Validación de cantidades

En las ventas, la cantidad debe ser mayor que cero.

Ejemplo:

```python
@field_validator("cantidad")
@classmethod
def validar_cantidad(cls, valor):
    if valor <= 0:
        raise ValueError(
            "La cantidad debe ser mayor que cero"
        )
    return valor
```

Esto evita registrar operaciones con cantidades inválidas como:

```text
0 unidades
-2 unidades
```

---

# 14. Routers y endpoints

FastAPI utiliza routers para organizar los endpoints por entidad.

Por ejemplo:

```text
/clientes
/categorias
/ofertas
/productos
/ventas
/detalle-ventas
```

Los routers reciben las solicitudes y utilizan los schemas correspondientes.

Un flujo de creación es:

```text
POST
 ↓
Router
 ↓
Schema / validación
 ↓
Modelo
 ↓
DAO
 ↓
PostgreSQL
```

Mientras que una consulta sigue:

```text
GET
 ↓
Router
 ↓
DAO
 ↓
PostgreSQL
 ↓
Respuesta
```

---

# 15. Manejo de errores

El backend utiliza excepciones personalizadas en los DAO para representar situaciones específicas.

Por ejemplo:

```text
ClienteNoEncontradoError
ProductoNoEncontradoError
```

También se pueden controlar errores relacionados con restricciones de la base de datos, especialmente las claves foráneas.

Los routers convierten estos errores en respuestas HTTP apropiadas mediante `HTTPException`.

Por ejemplo:

```python
raise HTTPException(
    status_code=404,
    detail="Registro no encontrado"
)
```

De esta forma, la API proporciona respuestas comprensibles al frontend.

---

# 16. Integridad referencial

PostgreSQL utiliza claves foráneas para mantener la integridad de las relaciones.

Por ejemplo:

```text
CLIENTE
   │
   └────── VENTA
```

y:

```text
VENTA
   │
   └────── DETALLE_VENTA
                  │
                  └────── PRODUCTO
```

Esto evita registrar relaciones con registros inexistentes.

También permite controlar operaciones que podrían dejar datos relacionados inconsistentes.

---

# 17. CORS

FastAPI utiliza `CORSMiddleware` para permitir la comunicación entre el backend y el frontend cuando se ejecutan en diferentes puertos.

Por ejemplo:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Esto permite que una aplicación frontend pueda realizar peticiones HTTP hacia nuestra API.

---

# 18. Archivo `main.py`

`main.py` funciona como punto de entrada de la aplicación.

Su responsabilidad principal es:

1. Crear la aplicación FastAPI.
2. Configurar CORS.
3. Inicializar la base de datos.
4. Registrar los routers.
5. Definir el endpoint principal.

La aplicación se ejecuta mediante Uvicorn.

Ejemplo:

```bash
uvicorn main:app --reload
```

---

# 19. Documentación automática

Una de las ventajas de FastAPI es que genera documentación automática de los endpoints.

Después de ejecutar el proyecto:

```bash
uvicorn main:app --reload
```

se puede acceder a:

```text
http://127.0.0.1:8000/docs
```

Esta interfaz permite:

* visualizar los endpoints;
* consultar los métodos HTTP;
* introducir datos;
* ejecutar solicitudes;
* revisar las respuestas;
* comprobar los códigos de estado.

También puede utilizarse la documentación alternativa disponible en:

```text
http://127.0.0.1:8000/redoc
```

---

# 20. Ejecución del backend

## Paso 1: instalar dependencias

```bash
python -m pip install fastapi
python -m pip install uvicorn
python -m pip install psycopg2-binary
python -m pip install pydantic
```

## Paso 2: configurar PostgreSQL

Crear la base de datos y configurar los datos de conexión:

```text
Host
Puerto
Nombre de la base de datos
Usuario
Contraseña
```

## Paso 3: ejecutar FastAPI

Desde la carpeta donde se encuentra `main.py`:

```bash
uvicorn main:app --reload
```

## Paso 4: abrir la documentación

Ingresar desde el navegador a:

```text
http://127.0.0.1:8000/docs
```

---

# 21. Flujo completo del sistema

El funcionamiento general del backend puede resumirse de la siguiente manera:

```text
                    FRONTEND
                       │
                       │ HTTP
                       ▼
                  ┌─────────┐
                  │ FastAPI │
                  └────┬────┘
                       │
                       ▼
                    Router
                       │
                       ▼
                    Schema
                       │
                 Validación
                       │
                       ▼
                    Modelo
                       │
                       ▼
                      DAO
                       │
                    psycopg2
                       │
                       ▼
                  PostgreSQL
                       │
                       ▼
                  Resultado
                       │
                       ▼
                    Router
                       │
                       ▼
                 Respuesta JSON
                       │
                       ▼
                    FRONTEND
```

---

# 22. Principales características del backend

El backend de TiendaIndieZone incorpora:

* API REST desarrollada con FastAPI.
* PostgreSQL como base de datos.
* Conexión mediante psycopg2.
* Arquitectura organizada por capas.
* Patrón DAO para acceso a datos.
* Schemas utilizando Pydantic.
* Validadores para controlar los datos recibidos.
* Modelos para representar las entidades.
* Routers separados por funcionalidad.
* Manejo de excepciones personalizadas.
* Integridad referencial mediante claves foráneas.
* Consultas SQL parametrizadas.
* Generación automática de identificadores mediante PostgreSQL.
* Uso de `RETURNING` para recuperar IDs generados.
* CORS para comunicación con el frontend.
* Documentación automática mediante Swagger.
* Ejecución mediante Uvicorn.
* Control de las reglas de negocio relacionadas con las ventas.

---

# 23. Conclusión

El backend de **TiendaIndieZone** está diseñado como una API REST independiente del frontend. Esta separación permite que la interfaz pueda comunicarse con el sistema mediante solicitudes HTTP sin acceder directamente a la base de datos.

La utilización de **FastAPI**, **Pydantic**, **DAO**, **psycopg2** y **PostgreSQL** permite mantener una estructura organizada, validar la información recibida y centralizar el acceso a los datos.

La arquitectura también facilita el mantenimiento del sistema, ya que cada componente tiene una responsabilidad definida y las operaciones de base de datos permanecen encapsuladas dentro de los DAO.
