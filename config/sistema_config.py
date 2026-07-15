from config.logger import Logger


class SistemaConfig:

    # Permite una única configuración del sistema
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

            # Registro del inicio del sistema
            Logger().info(
                f"Sistema iniciado: "
                f"{cls._instancia.nombre} | "
                f"Versión {cls._instancia.version}"
            )

        return cls._instancia