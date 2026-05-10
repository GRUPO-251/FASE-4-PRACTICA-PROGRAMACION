from datetime import datetime  # Importa la librería para manejar fechas y horas


# 1. ARCHIVO DE LOGS (Registro de eventos y errores)


def registrar_log(tipo, mensaje):
    """Guarda eventos en un archivo de texto"""
    try:
        archivo = open("sistema_logs.txt", "a", encoding="utf-8")
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"[{fecha_hora}] [{tipo.upper()}] {mensaje}\n")
    
    except IOError:
        print("CRÍTICO: No se pudo escribir en el archivo de logs.")
    
    finally:
        try:
            archivo.close()
        except NameError:
            pass


# 2. EXCEPCIONES PERSONALIZADAS


class ErrorSistemaFJ(Exception):
    """Clase base para errores del sistema"""
    pass

class ErrorValidacionDatos(ErrorSistemaFJ):
    """Error para fallos en los datos de entrada"""
    pass

class ErrorOperacionReserva(ErrorSistemaFJ):
    """Error para fallos en la lógica de reservas"""
    pass
