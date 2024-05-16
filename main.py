#Dependencias
#pip3 install paramiko
import paramiko

# Configuración de conexión
hostname = '122.122.124.1'
port = 22
username = 'admin'
password = '070523'

# IP del cliente en simple queue
cliente_ip = '122.122.124.98'
nueva_velocidad = '1k/1k'  # 1 kbps de subida y bajada

# Comando para ajustar la velocidad en simple queue
comando = f'/queue simple set [find target={cliente_ip}] max-limit={nueva_velocidad}'

def ejecutar_comando(hostname, port, username, password, comando):
    try:
        # Crear un cliente SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conectarse al MikroTik
        client.connect(hostname, port, username, password)
        
        # Ejecutar el comando
        stdin, stdout, stderr = client.exec_command(comando)
        
        # Leer la salida del comando
        salida = stdout.read().decode()
        errores = stderr.read().decode()
        
        # Cerrar la conexión
        client.close()
        
        if errores:
            print(f'Error: {errores}')
        else:
            print(f'Salida: {salida}')
    
    except Exception as e:
        print(f'Error al conectarse al MikroTik: {e}')

# Ejecutar el comando para cambiar la velocidad del cliente
ejecutar_comando(hostname, port, username, password, comando)
