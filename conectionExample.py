import paramiko

# Datos de conexión
hostname = '122.122.124.1'  # Dirección IP de tu MikroTik
port = 22  # Puerto SSH, generalmente es 22
username = 'admin'  # Usuario de tu MikroTik
password = '070523'  # Contraseña de tu MikroTik

# Crear una instancia del cliente SSH
client = paramiko.SSHClient()

# Agregar automáticamente la clave del servidor si no está en la lista de known hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Conectarse al dispositivo
    client.connect(hostname, port, username, password)
    
    # Ejecutar un comando
    stdin, stdout, stderr = client.exec_command('/system resource print')
    
    # Imprimir la salida del comando
    print(stdout.read().decode())

except Exception as e:
    print(f"Error: {e}")

finally:
    # Cerrar la conexión
    client.close()
