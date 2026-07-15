from config.logger import Logger


# Excepción cuando el cliente no existe
class ClienteNoEncontradoError(Exception):

    def __init__(self, id):
        super().__init__(f"Cliente ID={id} no encontrado")


# Excepción cuando el DNI ya existe
class DNIDuplicadoError(Exception):

    def __init__(self, dni):
        super().__init__(f"DNI '{dni}' ya registrado")


class ClienteDAO:

    def __init__(self):

        self.__bd = []          # Lista que simula la base de datos
        self.__cid = 1          # Contador de IDs
        self.__log = Logger()   # Instancia del Logger

    # Agrega un nuevo cliente
    def insertar(self, cliente):

        if self.buscar_por_dni(cliente.dni):
            raise DNIDuplicadoError(cliente.dni)

        cliente.id = self.__cid
        self.__cid += 1

        self.__bd.append(cliente)

        self.__log.info(
            f"Cliente agregado: {cliente.nombre} {cliente.apellido} "
            f"(ID={cliente.id})"
        )

        return cliente

    # Busca un cliente por DNI
    def buscar_por_dni(self, dni):

        for c in self.__bd:
            if c.dni == dni:
                return c

        return None

    # Busca un cliente por ID
    def buscar_por_id(self, id):

        for c in self.__bd:
            if c.id == id:
                return c

        return None

    # Devuelve la lista ordenada por nombre
    def obtener_todos(self):

        return sorted(
            self.__bd,
            key=lambda c: c.nombre
        )

    # Actualiza la información de un cliente
    def actualizar(
        self,
        id,
        nombre=None,
        apellido=None,
        dni=None,
        correo=None,
        telefono=None,
        fecha_registro=None
    ):

        cliente = self.buscar_por_id(id)

        if not cliente:

            self.__log.error(
                f"Actualizar fallido: Cliente ID={id} no existe"
            )

            raise ClienteNoEncontradoError(id)

        if dni and dni != cliente.dni:

            existente = self.buscar_por_dni(dni)

            if existente:
                raise DNIDuplicadoError(dni)

            cliente.dni = dni

        if nombre:
            cliente.nombre = nombre

        if apellido:
            cliente.apellido = apellido

        if correo:
            cliente.correo = correo

        if telefono:
            cliente.telefono = telefono

        if fecha_registro:
            cliente.fecha_registro = fecha_registro

        self.__log.info(
            f"Cliente actualizado: ID={id}"
        )

        return cliente

    # Elimina un cliente por ID
    def eliminar(self, id):

        cliente = self.buscar_por_id(id)

        if not cliente:

            self.__log.error(
                f"Eliminar fallido: Cliente ID={id} no existe"
            )

            raise ClienteNoEncontradoError(id)

        self.__bd.remove(cliente)

        self.__log.warning(
            f"Cliente eliminado: ID={id}"
        )