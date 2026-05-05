 from entidades_clientes import Servicio  # Importa la clase Servicio para aplicar herencia
from logs_excepciones import registrar_log, ErrorValidacionDatos, ErrorOperacionReserva, ErrorSistemaFJ  # Importa las herramientas de logs y errores

# =====================================================================
# 5. SERVICIOS ESPECIALIZADOS (Herencia, Polimorfismo y Sobrecarga)
# =====================================================================
class ServicioSala(Servicio):  # Clase que hereda de Servicio para representar el alquiler de salas
    def calcular_costo(self, horas, descuento=0.0):  # Implementa su propia forma de cobrar (Polimorfismo)
        subtotal = self.costo_base * horas  # Multiplica el precio base por el tiempo de uso
        total = subtotal - (subtotal * descuento)  # Aplica la reducción si se otorgó un descuento (Sobrecarga simulada)
        return round(total, 2)  # Devuelve el dinero redondeado a dos decimales

class ServicioEquipo(Servicio):  # Clase para representar el préstamo de proyectores o computadoras
    def calcular_costo(self, horas, descuento=0.0):  # Calcula el costo bajo sus propias reglas de negocio
        subtotal = (self.costo_base * horas) + 15.0  # Suma un valor fijo de $15 por mantenimiento del equipo
        total = subtotal - (subtotal * descuento)  # Aplica el porcentaje de descuento sobre el nuevo subtotal
        return round(total, 2)  # Devuelve el resultado final en formato decimal

class ServicioAsesoria(Servicio):  # Clase para representar el acompañamiento profesional
    def calcular_costo(self, horas, descuento=0.0):  # Resuelve el método obligatorio de cálculo de costos
        subtotal = self.costo_base * horas  # Obtiene el precio base por las horas agendadas
        total = (subtotal * 1.05) - (subtotal * descuento)  # Aplica un 5% de impuesto obligatorio antes del descuento
        return round(total, 2)  # Devuelve el cálculo final con precisión matemática

# =====================================================================
# 6. CLASE RESERVA (Manejo avanzado de Excepciones)
# =====================================================================
class Reserva:  # Clase principal que une a un Cliente con un Servicio solicitado
    def __init__(self, cliente, servicio, horas):  # Constructor que recibe los 3 datos clave
        self.cliente = cliente  # Guarda el objeto completo del cliente que solicita
        self.servicio = servicio  # Guarda el objeto del servicio que se está rentando
        if horas <= 0:  # Valida que el tiempo solicitado no sea cero ni negativo
            raise ErrorValidacionDatos("La duración en horas debe ser mayor a 0.")  # Lanza error si el tiempo es ilógico
        self.horas = horas  # Guarda la cantidad de tiempo de la reserva
        self.estado = "Pendiente"  # Asigna el estado inicial a toda nueva reserva

    def confirmar(self, descuento=0.0):  # Método para procesar el cobro y cerrar la reserva
        print(f"\n-> Procesando reserva de {self.cliente.get_nombre()}...")  # Avisa en pantalla el inicio del proceso
        try:  # Abre bloque try/except/else/finally exigido por la guía de la UNAD
            if self.estado == "Confirmada":  # Valida si la reserva ya fue pagada con anterioridad
                raise ErrorOperacionReserva("La reserva ya está confirmada.")  # Lanza error para evitar doble cobro
            if self.estado == "Cancelada":  # Valida si la reserva fue anulada previamente
                raise ErrorOperacionReserva("No se puede confirmar una reserva cancelada.")  # Lanza error de operación
            
            costo_final = self.servicio.calcular_costo(self.horas, descuento)  # Invoca el polimorfismo para calcular el costo
            
        except ErrorOperacionReserva as e:  # Captura los fallos lógicos específicos de la reserva
            registrar_log("error", f"Fallo al confirmar: {e}")  # Guarda el error exacto en el archivo de texto (Logs)
            raise ErrorSistemaFJ("No se pudo completar la operación") from e  # Aplica el encadenamiento obligatorio de errores
        except Exception as e:  # Captura cualquier otro error desconocido de Python
            registrar_log("error", f"Error inesperado: {e}")  # Registra el fallo desconocido en el archivo logs
            raise ErrorSistemaFJ("Fallo crítico en el cálculo") from e  # Lanza un error genérico ocultando los detalles técnicos
        else:  # Este bloque se activa únicamente si no ocurrió ninguna falla en el try
            self.estado = "Confirmada"  # Actualiza el estado de la reserva a Confirmada
            mensaje = f"Éxito: Reserva confirmada para {self.cliente.get_nombre()}. Total: ${costo_final}"  # Crea el reporte
            print(mensaje)  # Muestra el resultado positivo en la pantalla del usuario
            registrar_log("info", mensaje)  # Almacena el reporte exitoso en el archivo de texto
        finally:  # Se ejecuta SIEMPRE para cerrar el ciclo de atención de la reserva
            print(f"   [Sistema FJ] Finalizó revisión de reserva de {self.cliente.get_nombre()}.")  # Imprime el cierre

    def cancelar(self):  # Método para anular una reserva agendada
        print(f"\n-> Cancelando reserva de {self.cliente.get_nombre()}...")  # Avisa que inició el protocolo de anulación
        try:  # Abre el capturador de errores para la cancelación
            if self.estado == "Cancelada":  # Verifica si ya estaba cancelada de antes
                raise ErrorOperacionReserva("La reserva ya se encuentra cancelada.")  # Lanza error para no repetir la acción
            if self.estado == "Confirmada":  # Verifica si ya se pagó y se confirmó el servicio
                raise ErrorOperacionReserva("No se pueden cancelar reservas confirmadas.")  # Protege la lógica del negocio
                
            self.estado = "Cancelada"  # Actualiza el estado interno a Cancelada
            print(f"Éxito: La reserva de {self.cliente.get_nombre()} ha sido cancelada.")  # Informa al usuario en pantalla
            registrar_log("info", f"Reserva cancelada para {self.cliente.get_nombre()}")  # Registra la anulación en el archivo
            
        except ErrorOperacionReserva as e:  # Captura el fallo si se violaron las reglas de cancelación
            registrar_log("error", f"Error al cancelar: {e}")  # Apunta el intento fallido en el archivo logs
            raise ErrorSistemaFJ("Operación de cancelación fallida") from e  # Eleva el error encadenado hacia el sistema principal
        finally:  # Ejecuta el cierre visual obligatorio del bloque
            print(f"   [Sistema FJ] Finalizó intento de cancelación de {self.cliente.get_nombre()}.")  # Avisa el fin del intento
