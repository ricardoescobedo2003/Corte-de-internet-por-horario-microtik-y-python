import paramiko
import schedule
import time

def adjust_bandwidth_1():
    # Función para ajustar el ancho de banda a 1k/1k
    adjust_bandwidth('LNX', '1k/1k')

def adjust_bandwidth_2():
    # Función para ajustar el ancho de banda a 100M/15M
    adjust_bandwidth('LNX', '100M/15M')

def adjust_bandwidth(queue_name, new_max_limit):
    # Función para ajustar el ancho de banda
    hostname = '122.122.124.1'  # Dirección IP de tu MikroTik
    port = 22  # Puerto SSH, generalmente es 22
    username = 'admin'  # Usuario de tu MikroTik
    password = '070523'  # Contraseña de tu MikroTik

    # Comando para ajustar el ancho de banda
    command = f'/queue simple set [find name="{queue_name}"] max-limit={new_max_limit}'

    # Crear una instancia del cliente SSH
    client = paramiko.SSHClient()

    # Agregar automáticamente la clave del servidor si no está en la lista de known hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conectarse al dispositivo
        client.connect(hostname, port, username, password)
        
        # Ejecutar el comando para ajustar el ancho de banda
        stdin, stdout, stderr = client.exec_command(command)
        
        # Leer y mostrar la salida del comando, si es necesario
        output = stdout.read().decode()
        errors = stderr.read().decode()
        
        if output:
            print(f"Output: {output}")
        if errors:
            print(f"Errors: {errors}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cerrar la conexión
        client.close()

# Configurar el horario para ejecutar la función cada día a las 10:30PM y 5:50AM
schedule.every().day.at("19:27").do(adjust_bandwidth_1)
schedule.every().day.at("19:28").do(adjust_bandwidth_2)

print("Scheduler iniciado. Ejecutando cada día a las 10:30PM y 5:50AM...")

# Bucle infinito para mantener el script en ejecución y verificar el horario
while True:
    schedule.run_pending()
    time.sleep(1)
