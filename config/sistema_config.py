from config.logger import Logger


class SistemaConfig:

    _instancia = None

    def __new__(cls):

        if cls._instancia is None:

            cls._instancia = super().__new__(cls)

            cls._instancia.nombre = "TiendaIndieZone"
            cls._instancia.version = "1.0.0"
            cls._instancia.empresa = "Zone"

            cls._instancia.autores = (
                "Vega Campos Josias Aaron\n"
                "Rodas Roque Mariano"
            )

            # Crear el logger del sistema
            cls._instancia.logger = Logger()

            cls._instancia.logger.info(
                "Sistema iniciado correctamente."
            )

        return cls._instancia
