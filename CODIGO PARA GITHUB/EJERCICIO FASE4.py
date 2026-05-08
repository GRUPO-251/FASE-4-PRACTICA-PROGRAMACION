
from logs_excepciones import registrar_log, ErrorValidacionDatos, ErrorSistemaFJ  # Importa las funciones de logs y errores
from entidades_clientes import Cliente  # Importa la entidad Cliente para registrar nuevos usuarios
from servicios_reservas import ServicioSala, ServicioEquipo, ServicioAsesoria, Reserva  # Importa los servicios y la clase Reserva

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
                    raise ErrorSistemaFJ("No hay clientes registrados. Registre uno primero.")  # Frena el proceso
                
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
                    raise ErrorSistemaFJ("No hay reservas en el sistema.")  # Frena el proceso lanzando el error
                
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
