# IMPORTACIÓN Y CLASE ABSTRACTA

# Se importa ABC y abstractmethod desde el módulo abc
# ABC permite crear clases abstractas
# abstractmethod permite definir métodos obligatorios
from abc import ABC, abstractmethod


# Se define la clase abstracta Servicio
# Hereda de ABC para indicar que es una clase abstracta
class Servicio(ABC):

    # Constructor de la clase Servicio
    # Recibe el nombre del servicio
    def __init__(self, nombre):
        # Se guarda el nombre del servicio en el objeto
        self.nombre = nombre

    # Se define un método abstracto
    # Esto obliga a que las clases hijas lo implementen
    @abstractmethod
    def calcular_costo(self):
        # No se implementa aquí porque cada servicio tendrá su propio cálculo
        pass

# ETAPA 2: CLASE CLIENTE


# Se define la clase Cliente
class Cliente:

    # Constructor de la clase Cliente
    # Recibe nombre y correo
    def __init__(self, nombre, correo):

        # Bloque try para manejar errores sin que el programa se detenga
        try:
            # Validación: si el nombre está vacío
            if not nombre:
                # Se lanza un error personalizado
                raise ValueError("El nombre no puede estar vacío")

            # Validación: si el correo no contiene '@'
            if "@" not in correo:
                # Se lanza un error
                raise ValueError("Correo inválido")

            # Encapsulación:
            # Se usan dos guiones bajos para hacer atributos privados
            self.__nombre = nombre
            self.__correo = correo

        # Captura de errores tipo ValueError
        except ValueError as e:
            # Se muestra el error en pantalla
            print("Error al crear cliente:", e)

    # Método para obtener el nombre (getter)
    def get_nombre(self):
        # Retorna el nombre privado
        return self.__nombre

    # Método para obtener el correo (getter)
    def get_correo(self):
        # Retorna el correo privado
        return self.__correo


# ================================
# PRUEBA BÁSICA (OPCIONAL)
# ================================

# Se ejecuta solo si este archivo es el principal
if __name__ == "__main__":

    # Creación de un cliente válido
    cliente1 = Cliente("Andres", "andres@gmail.com")

    # Se imprime el nombre del cliente usando el getter
    print("Cliente creado:", cliente1.get_nombre())

    # Creación de un cliente con error (nombre vacío)
    cliente2 = Cliente("", "correo@gmail.com")

    # Creación de un cliente con error (correo inválido)
    cliente3 = Cliente("Pedro", "correo_sin_arroba")