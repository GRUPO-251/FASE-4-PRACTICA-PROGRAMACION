from abc import ABC, abstractmethod
from datetime import datetime
from logs_excepciones import ErrorValidacionDatos

# =====================================================================
# 3. CLASES ABSTRACTAS Y ENTIDADES
# =====================================================================

class EntidadSistema(ABC):
    """Clase abstracta base para entidades del sistema"""

    def __init__(self):
        self.fecha_registro = datetime.now()

    @abstractmethod
    def obtener_descripcion(self):
        pass


class Servicio(EntidadSistema):
    """Clase abstracta para los servicios"""

    def __init__(self, nombre, costo_base):
        super().__init__()
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, horas, descuento=0.0):
        pass

    def obtener_descripcion(self):
        return f"Servicio: {self.nombre} | Costo Base: ${self.costo_base}"


# =====================================================================
# 4. CLASE CLIENTE (Encapsulación y validación)
# =====================================================================

class Cliente(EntidadSistema):
    """Clase para representar clientes del sistema"""

    def __init__(self, nombre, correo):
        super().__init__()

        if not nombre or len(nombre.strip()) < 3:
            raise ErrorValidacionDatos(
                "El nombre debe tener al menos 3 caracteres."
            )

        if "@" not in correo or "." not in correo:
            raise ErrorValidacionDatos(
                "El correo electrónico no es válido."
            )

        self.__nombre = nombre
        self.__correo = correo

    def get_nombre(self):
        return self.__nombre

    def obtener_descripcion(self):
        return f"Cliente: {self.__nombre} | Email: {self.__correo}"
