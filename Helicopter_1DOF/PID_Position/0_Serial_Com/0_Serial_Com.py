import serial
import serial.tools.list_ports
import threading
import csv
import os
import time

# --- CONFIGURACIÓN ---
BAUD_RATE = 115200
FOLDER_NAME = "Results"
FILE_NAME = "telemetria.csv"

FULL_PATH = os.path.join(os.path.dirname(__file__), FOLDER_NAME, FILE_NAME)

def Initialize_CSV():
    """Crea la carpeta y el archivo desde cero con su encabezado."""
    directorio = os.path.dirname(FULL_PATH)
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    # Abrimos con 'w' para SOBREESCRIBIR cualquier experimento previo
    with open(FULL_PATH, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp_MS", "Angulo", "PWM", "Modo"])
    print(f"Archivo {FILE_NAME} inicializado (limpio).")

def Save_CSV_File(data_row):
    """Añade una fila al archivo existente."""
    # Usamos 'a' (append) porque el archivo ya fue creado/limpiado por Initialize_CSV
    with open(FULL_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)

def read_serial_thread(ser):
    """Hilo secundario: Lee el puerto y guarda en el archivo."""
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                partes = line.split(',')
                if len(partes) == 4:
                    Save_CSV_File(partes)
        except:
            break

def mostrar_ayuda():
    """Muestra el menú de comandos disponibles."""
    print("\n" + "="*30)
    print("      AYUDA DE COMANDOS")
    print("="*30)
    print("CAL      : Calibrar sensor")
    print("M:<val>  : Cambiar consigna (ej: M:12.5)")
    print("I        : Poner en estado IDLE")
    print("FREQ:<ms>: Cambiar frecuencia de envío")
    print("help     : Mostrar este menú")
    print("q        : Enviar 'I' y SALIR")
    print("="*30 + "\n")

def main():
    # 1. Limpiar/Crear el archivo antes de empezar cualquier lectura
    Initialize_CSV()

    # Listar puertos disponibles
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No se detectaron dispositivos seriales.")
        return

    for i, p in enumerate(ports): 
        print(f"[{i}] {p.device} - {p.description}")
    
    try:
        idx = int(input("\nSelecciona el índice del puerto: "))
        puerto_nombre = ports[idx].device
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    # Abrir conexión
    try:
        ser = serial.Serial(puerto_nombre, BAUD_RATE, timeout=0.1)
    except Exception as e:
        print(f"Error al conectar: {e}")
        return

    # Lanzar hilo de lectura en segundo plano
    threading.Thread(target=read_serial_thread, args=(ser,), daemon=True).start()

    print(f"\nConectado a {puerto_nombre}")
    print(f"Guardando métricas en: {FULL_PATH}")
    print("Escribe 'help' para comandos o 'q' para salir.")

    while True:
        cmd = input("TX > ").strip()
        
        if not cmd:
            continue

        if cmd.lower() == 'q':
            print("Enviando comando 'I' (Idle) antes de cerrar...")
            ser.write(b"I\n") 
            time.sleep(0.1)   
            break
        
        elif cmd.lower() == 'help':
            mostrar_ayuda()
        
        else:
            ser.write(f"{cmd}\n".encode())

    ser.close()
    print("Conexión cerrada. Programa finalizado.")

if __name__ == "__main__":
    print("\n\n")
    main()