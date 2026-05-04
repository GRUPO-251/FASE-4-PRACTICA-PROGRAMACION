from abc import ABC, abstractmethod  # Importa las herramientas para crear clases abstractas obligatorias
from datetime import datetime  # Importa la librería para manejar fechas y horas actuales

# =====================================================================
# 1. ARCHIVO DE LOGS (Registro de eventos y errores)
# =====================================================================
def registrar_log(tipo, mensaje):  # Define la función para guardar eventos en el archivo de texto
    try:  # Inicia un bloque de prueba para intentar abrir y escribir el archivo
        archivo = open("sistema_logs.txt", "a", encoding="utf-8")  # Abre el archivo en modo "añadir" sin borrar lo anterior
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtiene el momento exacto y le da formato legible
        archivo.write(f"[{fecha_hora}] [{tipo.upper()}] {mensaje}\n")  # Escribe la línea con fecha, tipo y el mensaje
    except IOError:  # Si ocurre un error de entrada/salida (como falta de permisos) se activa esta parte
        print("CRÍTICO: No se pudo escribir en el archivo de logs.")  # Informa en pantalla que no se pudo guardar el log
    finally:  # Bloque que se ejecuta de forma obligatoria falle o no el proceso anterior
        try:  # Intenta cerrar el archivo de forma segura
            archivo.close()  # Cierra el archivo liberando la memoria del computador
        except NameError:  # Se activa si la variable 'archivo' no llegó a crearse
            pass  # No hace nada y permite continuar con la ejecución del programa

# =====================================================================
# 2. EXCEPCIONES PERSONALIZADAS
# =====================================================================
class ErrorSistemaFJ(Exception):  # Crea nuestra propia clase base de errores heredando de Exception
    pass  # No requiere código interno, funciona solo como un nuevo tipo de error

class ErrorValidacionDatos(ErrorSistemaFJ):  # Crea un error específico para fallos en los datos de entrada
    pass  # Hereda de nuestra clase de error base

class ErrorOperacionReserva(ErrorSistemaFJ):  # Crea un error específico para fallos en la lógica de las reservas
    pass  # Funciona como identificador para capturar fallos lógicos del negocio

# =====================================================================
# 3. CLASES ABSTRACTAS Y ENTIDADES
# =====================================================================
class EntidadSistema(ABC):  # Define una clase abstracta para las entidades generales del software
    def __init__(self):  # Constructor que se ejecuta al nacer un objeto de esta clase
        self.fecha_registro = datetime.now()  # Guarda automáticamente el momento en que se crea el objeto
    
    @abstractmethod  # Indica que el siguiente método es obligatorio para las clases hijas
    def obtener_descripcion(self):  # Método que obligará a describir los objetos creados
        pass  # No se programa nada aquí porque se desarrollará en las clases hijas

class Servicio(EntidadSistema):  # Clase abstracta que representa a los servicios que ofrece la empresa
    def __init__(self, nombre, costo_base):  # Constructor que recibe el nombre y el precio por hora
        super().__init__()  # Llama al constructor de la clase padre (EntidadSistema)
        self.nombre = nombre  # Guarda el nombre del servicio recibido como parámetro
        self.costo_base = costo_base  # Guarda el costo base por hora del servicio

    @abstractmethod  # Obliga a calcular el costo de forma individual en cada hijo
    def calcular_costo(self, horas, descuento=0.0):  # Firma del método que calculará los precios
        pass  # Se deja vacío para ser resuelto mediante polimorfismo

    def obtener_descripcion(self):  # Implementa la descripción obligatoria para los servicios
        return f"Servicio: {self.nombre} | Costo Base: ${self.costo_base}"  # Devuelve texto con los datos básicos

# =====================================================================
# 4. CLASE CLIENTE (Encapsulación y validación)
# =====================================================================
class Cliente(EntidadSistema):  # Clase para representar a los usuarios que compran servicios
    def __init__(self, nombre, correo):  # Constructor que recibe el nombre y el email del cliente
        super().__init__()  # Llama a la clase padre para registrar la fecha de creación
        if not nombre or len(nombre.strip()) < 3:  # Valida que el nombre no esté vacío ni tenga menos de 3 letras
            raise ErrorValidacionDatos("El nombre debe tener al menos 3 caracteres.")  # Lanza nuestro error personalizado
        if "@" not in correo or "." not in correo:  # Valida que el correo tenga estructura básica con @ y punto
            raise ErrorValidacionDatos("El correo electrónico no es válido.")  # Lanza error si el email no es real
            
        self.__nombre = nombre  # Atributo privado con doble guion bajo (Encapsulamiento)
        self.__correo = correo  # Atributo privado que guarda el email de forma segura

    def get_nombre(self):  # Método público para poder leer el nombre privado del cliente
        return self.__nombre  # Devuelve el nombre protegido hacia el exterior

    def obtener_descripcion(self):  # Implementa la descripción obligatoria para los clientes
        return f"Cliente: {self.__nombre} | Email: {self.__correo}"  # Devuelve la ficha del cliente en texto

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

# =====================================================================
# 7. MENÚ INTERACTIVO Y OPERACIÓN DEL SISTEMA
# =====================================================================
def ejecutar_programa():  # Define la función principal que controla la aplicación
    clientes = []  # Crea la lista en blanco para guardar a los clientes en memoria
    reservas = []  # Crea la lista en blanco para almacenar las reservas generadas
    servicios = [  # Crea una lista de objetos precargados con los servicios fijos del negocio
        ServicioSala("Sala de Juntas", 50.0),  # Instancia el servicio de sala a $50 la hora
        ServicioEquipo("Alquiler Proyector", 20.0),  # Instancia el servicio de equipos a $20 la hora
        ServicioAsesoria("Asesoría TI", 80.0)  # Instancia el servicio de asesoría a $80 la hora
    ]  # Cierra la lista de servicios disponibles
    
    registrar_log("info", "--- Inicio de sesión de usuario ---")  # Guarda el arranque del sistema en los logs

    while True:  # Crea un bucle infinito para que el menú no se cierre tras cada acción
        print("\n==========================================")  # Imprime un separador gráfico en consola
        print("       SISTEMA DE GESTIÓN - SOFTWARE FJ")  # Título de la aplicación en pantalla
        print("==========================================")  # Imprime un separador gráfico en consola
        print("1. Registrar Cliente")  # Muestra la opción número 1
        print("2. Crear y Confirmar Reserva")  # Muestra la opción número 2
        print("3. Cancelar Reserva")  # Muestra la opción número 3
        print("4. Ver Clientes Registrados")  # Muestra la opción número 4
        print("5. Ver Reservas")  # Muestra la opción número 5
        print("6. Salir")  # Muestra la opción número 6 para cerrar la aplicación
        print("==========================================")  # Imprime la línea de cierre del menú
        
        opcion = input("Seleccione una opción: ")  # Captura el texto que digite el usuario en consola
        
        try:  # Abre el gran capturador de errores de la interfaz para que el menú nunca se cierre
            if opcion == "1":  # Verifica si el usuario digitó el número 1
                print("\n--- REGISTRO DE CLIENTE ---")  # Imprime el encabezado del módulo de clientes
                nombre = input("Ingrese nombre: ")  # Captura el nombre escrito por el usuario
                correo = input("Ingrese correo: ")  # Captura el email escrito por el usuario
                
                nuevo_cliente = Cliente(nombre, correo)  # Crea un nuevo objeto Cliente (Aquí se aplican las validaciones)
                clientes.append(nuevo_cliente)  # Añade el cliente exitoso a la lista de memoria
                print(f"Éxito: Cliente {nombre} registrado correctamente.")  # Informa el éxito de la acción
                registrar_log("info", f"Cliente registrado: {nombre}")  # Apunta el evento en el archivo de texto
                
            elif opcion == "2":  # Verifica si el usuario digitó el número 2
                print("\n--- CREACIÓN DE RESERVA ---")  # Imprime el encabezado del módulo de reservas
                if not clientes:  # Valida si no hay clientes registrados todavía en la lista
                    raise ErrorOperacionReserva("No hay clientes registrados. Registre uno primero.")  # Frena el proceso
                
                print("Clientes disponibles:")  # Enlista en pantalla los clientes listos
                for i, c in enumerate(clientes):  # Recorre la lista de clientes obteniendo su posición
                    print(f"{i}. {c.get_nombre()}")  # Muestra el número índice y el nombre de cada cliente
                idx_c = int(input("Seleccione el número del cliente: "))  # Captura y transforma a entero la selección
                
                print("\nServicios disponibles:")  # Enlista los servicios que ofrece la empresa
                for i, s in enumerate(servicios):  # Recorre la lista de servicios con su posición
                    print(f"{i}. {s.nombre} (${s.costo_base}/h)")  # Muestra el índice, nombre y costo por hora
                idx_s = int(input("Seleccione el número del servicio: "))  # Transforma a número entero la selección del usuario
                
                horas = float(input("Ingrese la duración en horas: "))  # Captura el tiempo y lo convierte a número decimal
                descuento = float(input("Ingrese porcentaje de descuento (Ej: 0.10 para 10% o 0 para ninguno): "))  # Captura el porcentaje
                
                nueva_reserva = Reserva(clientes[idx_c], servicios[idx_s], horas)  # Crea el objeto Reserva vinculando los datos
                nueva_reserva.confirmar(descuento)  # Ejecuta el cobro y activa el try/except interno de la reserva
                reservas.append(nueva_reserva)  # Añade la reserva completada a la lista de memoria
                
            elif opcion == "3":  # Verifica si el usuario digitó el número 3
                print("\n--- CANCELACIÓN DE RESERVA ---")  # Imprime el encabezado de anulaciones
                if not reservas:  # Valida si no hay ninguna reserva guardada todavía
                    raise ErrorOperacionReserva("No hay reservas en el sistema.")  # Frena el proceso lanzando el error
                
                for i, r in enumerate(reservas):  # Recorre las reservas con sus posiciones numéricas
                    print(f"{i}. {r.cliente.get_nombre()} - {r.servicio.nombre} [Estado: {r.estado}]")  # Imprime la ficha resumida
                idx_r = int(input("Seleccione el número de la reserva a cancelar: "))  # Captura el número entero de la reserva
                
                reservas[idx_r].cancelar()  # Llama al método cancelar del objeto reserva seleccionado
                
            elif opcion == "4":  # Verifica si el usuario digitó el número 4
                print("\n--- LISTA DE CLIENTES ---")  # Imprime el título del listado
                if not clientes: print("No hay clientes.")  # Mensaje rápido si la lista está vacía
                for c in clientes: print(c.obtener_descripcion())  # Recorre e imprime la descripción de cada cliente
                
            elif opcion == "5":  # Verifica si el usuario digitó el número 5
                print("\n--- LISTA DE RESERVAS ---")  # Imprime el título de la bitácora
                if not reservas: print("No hay reservas.")  # Mensaje rápido si no hay ninguna reserva hecha
                for r in reservas:  # Recorre la lista de reservas efectuadas
                    print(f"Cliente: {r.cliente.get_nombre()} | {r.servicio.nombre} | Horas: {r.horas} | Estado: {r.estado}")  # Muestra los datos
                    
            elif opcion == "6":  # Verifica si el usuario digitó el número 6
                print("\n¡Gracias por usar el Sistema FJ! Cerrando...")  # Mensaje de despedida
                registrar_log("info", "--- Fin de la sesión de usuario ---")  # Registra el apagado del software en los logs
                break  # Rompe el bucle While True terminando definitivamente la ejecución
            
            else:  # Se activa si el usuario digitó un número que no estaba en el menú (ej. 7 u 8)
                print("Opción no válida. Intente de nuevo.")  # Alerta al usuario para que corrija

        except (ErrorValidacionDatos, ErrorSistemaFJ) as e:  # Captura los errores que nosotros programamos a mano
            print(f"\n[ERROR CONTROLADO]: {e}")  # Muestra el error de negocio sin romper la aplicación
        except ValueError:  # Captura si el usuario metió letras donde el programa pedía números
            print("\n[ERROR CONTROLADO]: Debe ingresar un número válido para las listas o las horas.")  # Alerta del error tipográfico
        except IndexError:  # Captura si el usuario metió un número que no existía en la lista de opciones
            print("\n[ERROR CONTROLADO]: El número seleccionado no existe en la lista.")  # Advierte del error posicional
        except Exception as e:  # Captura de última instancia para cualquier otra falla imprevista
            print(f"\n[ERROR CONTROLADO INESPERADO]: {e}")  # Muestra la falla técnica sin congelar la pantalla

if __name__ == "__main__":  # Valida si este archivo se está ejecutando directamente y no importando
    ejecutar_programa()  # Arranca el software llamando a la función del menú interactivo