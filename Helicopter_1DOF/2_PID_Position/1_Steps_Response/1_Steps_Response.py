"""
Experimento que envía una secuencia de escalones al ESC y registra la respuesta del sistema.

Flujo:
  1. Conecta al puerto COM del ESP32 S3.
  2. Pregunta si calibrar el ESC (CAL) [Y/N].
  3. Pregunta si iniciar el sistema [S/N].
  4. Inicializa el archivo CSV en la carpeta Results/.
  5. Ejecuta la secuencia de escalones definida en ESCALONES.
  6. Registra: Timestamp_MS, Angulo, PWM_Reportado, Modo, Escalon_Set, Timestamp_Python

Interrupción segura:
  - Presione 'q' o 'I' seguido de Enter para detener el motor.
"""

import serial
import serial.tools.list_ports
import threading
import csv
import os
import time
import sys

# --- CONFIGURACIÓN ---
BAUD_RATE = 115200
STEP_DURATION = 10.0  # Segundos por cada escalón
#ESCALONES = [0, 10, 20, 30, 40, 30, 20, 10, 0] 
#ESCALONES = [0, 5, 10, 15, 20, 25, 30, 35, 40, 35, 30, 25, 20, 15, 10, 5, 0]
#ESCALONES = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 37.5, 35, 32.5, 30, 27.5, 25, 22.5, 20, 17.5, 15, 12.5, 10, 7.5, 5, 2.5, 0]
ESCALONES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11,10 ,9 ,8 ,7 ,6 ,5 ,4 ,3 ,2 ,1 ,0]
FOLDER_NAME = "Results"
FILE_NAME = "1_results_steps_response.csv"

BASE_DIR = os.path.dirname(__file__)
FULL_PATH = os.path.join(BASE_DIR, FOLDER_NAME, FILE_NAME)

# Variables de control
current_step_pct = 0
experiment_running = True

def Initialize_CSV():
    """Crea la carpeta y el archivo con su encabezado."""
    directorio = os.path.dirname(FULL_PATH)
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    with open(FULL_PATH, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp_MS", "Angulo", "PWM_Reportado", "Modo", "Escalon_Set", "Timestamp_Python"])
    print(f"\nArchivo inicializado: {FULL_PATH}")

def Save_CSV_Row(partes):
    """Añade una fila de datos al CSV."""
    with open(FULL_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(partes + [current_step_pct, round(time.time(), 4)])

def read_serial_thread(ser):
    """Hilo secundario para lectura constante del puerto serial."""
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                partes = line.split(',')
                if len(partes) == 4:
                    Save_CSV_Row(partes)
        except:
            break

def monitor_input_thread(ser):
    """Hilo para detectar interrupción del usuario ('q' o 'I')."""
    global experiment_running
    while experiment_running:
        user_input = input().strip().lower()
        if user_input in ['q', 'i']:
            print("\n!!! Interrupción detectada. Deteniendo motor...")
            ser.write(b"I\n")
            experiment_running = False
            break

def main():
    global current_step_pct, experiment_running
    
    # --- 1. Selección de puerto ---
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No se detectaron puertos seriales.")
        return
    
    print("\nPuertos disponibles:")
    for i, p in enumerate(ports): 
        print(f"  [{i}] {p.device} - {p.description}")
    
    try:
        idx = int(input("\nSelecciona el índice del puerto: "))
        ser = serial.Serial(ports[idx].device, BAUD_RATE, timeout=0.1)
    except Exception as e:
        print(f"Error de conexión: {e}")
        return

    # --- 2. Preguntas de configuración ---
    # Calibración (Solo Y o N)
    while True:
        cal_resp = input("¿Desea calibrar el ESC? (Y/N): ").strip().upper()
        if cal_resp in ['Y', 'N']:
            break
        print("Entrada no válida. Use 'Y' para Sí o 'N' para No.")

    if cal_resp == 'Y':
        print("Calibrando... Espere confirmación sonora.")
        ser.write(b"CAL\n")
        time.sleep(3.5)

    # Iniciar Sistema (Solo S o N)
    while True:
        start_resp = input("¿Desea iniciar el sistema y el experimento? (S/N): ").strip().upper()
        if start_resp in ['S', 'N']:
            break
        print("Entrada no válida. Use 'S' para iniciar o 'N' para cancelar.")

    if start_resp == 'N':
        print("Experimento cancelado por el usuario.")
        ser.close()
        return

    # --- 3. Inicio del Experimento ---
    Initialize_CSV()
    
    # Lanzar hilos de monitoreo
    threading.Thread(target=read_serial_thread, args=(ser,), daemon=True).start()
    threading.Thread(target=monitor_input_thread, args=(ser,), daemon=True).start()

    print("\n--- Ejecutando Secuencia ---")
    print("Presione 'q' + Enter para abortar en cualquier momento.")

    for pct in ESCALONES:
        if not experiment_running: 
            break
        
        current_step_pct = pct
        print(f"  -> M:{pct} | Duración: {STEP_DURATION}s")
        ser.write(f"M:{pct}\n".encode())
        
        # Espera segmentada para interrupción inmediata
        for _ in range(int(STEP_DURATION * 10)):
            if not experiment_running: 
                break
            time.sleep(0.1)

    # --- 4. Finalización ---
    ser.write(b"I\n")
    experiment_running = False
    ser.close()
    print("\nExperimento finalizado correctamente. Conexión cerrada.")

if __name__ == "__main__":
    main()