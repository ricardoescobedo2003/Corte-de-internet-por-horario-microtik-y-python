import tkinter as tk
from tkinter import ttk
import paramiko
import schedule
import time

def adjust_bandwidth():
    # Función para ajustar el ancho de banda
    hostname = hostname_entry.get()
    port = 22  # Puerto SSH, generalmente es 22
    username = username_entry.get()
    password = password_entry.get()
    queue_name = queue_entry.get()
    new_max_limit = limit_entry.get()

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
            result_label.config(text=f"Output: {output}")
        if errors:
            result_label.config(text=f"Errors: {errors}")

    except Exception as e:
        result_label.config(text=f"Error: {e}")

    finally:
        # Cerrar la conexión
        client.close()

def schedule_task():
    # Función para programar la tarea según el horario especificado
    schedule_time = time_entry.get()
    schedule.every().day.at(schedule_time).do(adjust_bandwidth)
    result_label.config(text=f"Tarea programada para las {schedule_time}")

# Crear la ventana principal
root = tk.Tk()
root.title("Ajuste de Ancho de Banda")

# Crear y posicionar los elementos en la ventana
tk.Label(root, text="Hostname:").grid(row=0, column=0)
hostname_entry = tk.Entry(root)
hostname_entry.grid(row=0, column=1)

tk.Label(root, text="Username:").grid(row=1, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1)

tk.Label(root, text="Password:").grid(row=2, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1)

tk.Label(root, text="Nombre de Queue:").grid(row=3, column=0)
queue_entry = tk.Entry(root)
queue_entry.grid(row=3, column=1)

tk.Label(root, text="Límite de Ancho de Banda:").grid(row=4, column=0)
limit_entry = tk.Entry(root)
limit_entry.grid(row=4, column=1)

tk.Label(root, text="Horario (HH:MM):").grid(row=5, column=0)
time_entry = tk.Entry(root)
time_entry.grid(row=5, column=1)

schedule_button = tk.Button(root, text="Programar Tarea", command=schedule_task)
schedule_button.grid(row=6, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=7, column=0, columnspan=2)

# Iniciar el bucle de la aplicación
root.mainloop()
