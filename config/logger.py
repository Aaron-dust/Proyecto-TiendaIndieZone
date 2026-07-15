import datetime


class Logger:

    # Implementación del patrón Singleton
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._logs = []
        return cls._instancia

    # Registra un evento en el historial
    def _registrar(self, nivel, mensaje):

        hora = datetime.datetime.now().strftime("%H:%M:%S")

        entrada = {
            "hora": hora,
            "nivel": nivel,
            "msg": mensaje
        }

        self._logs.append(entrada)

    def info(self, mensaje):
        self._registrar("INFO", mensaje)

    def warning(self, mensaje):
        self._registrar("WARNING", mensaje)

    def error(self, mensaje):
        self._registrar("ERROR", mensaje)

    # Muestra el historial de eventos
    def mostrar_logs(self):

        print(f"\n========== HISTORIAL DEL SISTEMA ({len(self._logs)} eventos) ==========")

        for log in self._logs:
            print(f"[{log['hora']}] {log['nivel']:7} | {log['msg']}")

    # Elimina todos los registros del historial
    def limpiar(self):

        self._logs.clear()

        print("Historial del sistema eliminado correctamente.")