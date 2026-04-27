
# IMPORTACIONES
# Importa herramientas para crear clases abstractas
from abc import ABC, abstractmethod

# EXCEPCIÓN PERSONALIZADA
# Se crea una clase de error propia del sistema
class ErrorSistema(Exception):
    pass  # No hace nada, solo sirve como tipo de error


# CLASE ABSTRACTA SERVICIO
# Clase abstracta (no se puede usar directamente)
class Servicio(ABC):

    # Constructor que recibe el nombre del servicio
    def __init__(self, nombre):
        self.nombre = nombre  # Guarda el nombre

    # Método abstracto (obligatorio en las clases hijas)
    @abstractmethod
    def calcular_costo(self):
        pass  # No se implementa aquí


# CLASE CLIENTE

class Cliente:

    # Constructor con nombre y correo
    def __init__(self, nombre, correo):

        # Validación: si el nombre está vacío
        if not nombre:
            raise ValueError("Nombre vacío")  # Lanza error

        # Validación: si el correo no tiene @
        if "@" not in correo:
            raise ValueError("Correo inválido")  # Lanza error

        # Encapsulación: atributos privados
        self.__nombre = nombre
        self.__correo = correo

    # Método para obtener el nombre
    def get_nombre(self):
        return self.__nombre


# SERVICIOS (HERENCIA Y POLIMORFISMO)

# Servicio de tipo Sala
class ServicioSala(Servicio):

    # Implementa el método obligatorio
    def calcular_costo(self):
        return 100  # Costo fijo


# Servicio de tipo Equipo
class ServicioEquipo(Servicio):

    def calcular_costo(self):
        return 200


# Servicio de tipo Asesoría
class ServicioAsesoria(Servicio):

    def calcular_costo(self):
        return 300

# CLASE RESERVA


class Reserva:

    # Constructor recibe cliente y servicio
    def __init__(self, cliente, servicio):
        self.cliente = cliente  # Guarda cliente
        self.servicio = servicio  # Guarda servicio
        self.estado = "Pendiente"  # Estado inicial

    # Método para confirmar la reserva
    def confirmar(self):

        # Bloque para manejar errores
        try:
            # Llama al método del servicio (polimorfismo)
            costo = self.servicio.calcular_costo()

            # Cambia el estado
            self.estado = "Confirmada"

            # Muestra mensaje
            print(f"Reserva confirmada para {self.cliente.get_nombre()} - Costo: {costo}")

        # Si ocurre error
        except Exception as e:
            print("Error en la reserva:", e)

        # Siempre se ejecuta
        finally:
            print("Proceso finalizado\n")


# FUNCIÓN PRINCIPAL (SIMULACIÓN)

def main():

    print("INICIO DEL SISTEMA\n")

    try:
        # Cliente correcto
        c1 = Cliente("Andres", "andres@gmail.com")

        # Crear servicios
        s1 = ServicioSala("Sala")
        s2 = ServicioEquipo("Equipo")

        # Crear reservas
        r1 = Reserva(c1, s1)
        r1.confirmar()  # Ejecuta

        r2 = Reserva(c1, s2)
        r2.confirmar()

        # ERROR INTENCIONAL (nombre vacío)
        c2 = Cliente("", "correo@gmail.com")

    except ValueError as e:
        print("Error detectado:", e)

    finally:
        print("FIN DEL SISTEMA")



# EJECUCIÓN DEL PROGRAMA

# Llama a la función principal
main()