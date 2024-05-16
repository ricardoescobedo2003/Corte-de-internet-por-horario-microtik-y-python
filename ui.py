import paramiko
import schedule
import time
import tkinter as tk
from tkinter import messagebox

def adjust_bandwidth(queue_name, new_max_limit, hostname, username, password):
    port = 22  # Puerto SSH, generalmente es 22
    command = f'/queue simple set [find name="{queue_name}"] max-limit={new_max_limit}'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, port, username, password)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        errors = stderr.read().decode()
        
        if output:
            print(f"Output: {output}")
        if errors:
            print(f"Errors: {errors}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()

def schedule_bandwidth_change(queue_name, first_limit, start_time, second_limit, end_time, hostname, username, password):
    schedule.every().day.at(start_time).do(adjust_bandwidth, queue_name, first_limit, hostname, username, password)
    schedule.every().day.at(end_time).do(adjust_bandwidth, queue_name, second_limit, hostname, username, password)
    messagebox.showinfo("Scheduler", f"Scheduler iniciado. Ejecutando ajustes de ancho de banda a las {start_time} y {end_time}...")
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    hostname = entry_hostname.get()
    username = entry_username.get()
    password = entry_password.get()
    queue_name = entry_queue_name.get()
    start_time = entry_start_time.get()
    first_limit = entry_first_limit.get()
    end_time = entry_end_time.get()
    second_limit = entry_second_limit.get()

    if not all([hostname, username, password, queue_name, start_time, first_limit, end_time, second_limit]):
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    root.after(100, schedule_bandwidth_change, queue_name, first_limit, start_time, second_limit, end_time, hostname, username, password)

root = tk.Tk()
root.title("Ajuste de Ancho de Banda para MikroTik")

tk.Label(root, text="Hostname/IP:").grid(row=0, column=0, padx=5, pady=5)
entry_hostname = tk.Entry(root)
entry_hostname.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Usuario:").grid(row=1, column=0, padx=5, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Nombre de la Queue:").grid(row=3, column=0, padx=5, pady=5)
entry_queue_name = tk.Entry(root)
entry_queue_name.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Hora de Inicio (HH:MM):").grid(row=4, column=0, padx=5, pady=5)
entry_start_time = tk.Entry(root)
entry_start_time.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Primer Límite de Ancho de Banda (ej. 1k/1k):").grid(row=5, column=0, padx=5, pady=5)
entry_first_limit = tk.Entry(root)
entry_first_limit.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Hora de Fin (HH:MM):").grid(row=6, column=0, padx=5, pady=5)
entry_end_time = tk.Entry(root)
entry_end_time.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Segundo Límite de Ancho de Banda (ej. 100M/15M):").grid(row=7, column=0, padx=5, pady=5)
entry_second_limit = tk.Entry(root)
entry_second_limit.grid(row=7, column=1, padx=5, pady=5)

tk.Button(root, text="Iniciar Scheduler", command=start_scheduler).grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
