import serial
import serial.tools.list_ports
import csv
import os
import threading
import time
import sys
import numpy as np
from queue import Empty, Queue

# =============================================================================
# TEORÍA DEL MÉTODO DEL RELÉ (ASTRÖM-HÄGGLUND)
# =============================================================================
# Ku = (4 * d) / (π * sqrt(a^2 - ε^2))
# Donde d: Amplitud relé, a: Amplitud oscilación, ε: Histéresis.
# =============================================================================

# --- CONFIGURACIÓN DE ARCHIVOS (Referencia 1_Steps_Response) ---
BAUD_RATE = 115200
DT_CONTROL = 0.01 
U_MIN, U_MAX = 0.0, 50.0 

FOLDER_NAME = "Results"
FILE_NAME = "2_results_rele.csv"
BASE_DIR = os.path.dirname(__file__)
FULL_PATH = os.path.join(BASE_DIR, FOLDER_NAME, FILE_NAME)

# Variables globales para persistencia en Save_CSV_Row
current_u = 0.0
current_ref = 0.0

def Initialize_CSV():
    """Crea la carpeta y el archivo con su encabezado (Referencia 1_Steps_Response)."""
    directorio = os.path.dirname(FULL_PATH)
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    with open(FULL_PATH, mode='w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        # Encabezado adaptado para el experimento de Relé
        writer.writerow(["t_s", "ref", "angulo", "error", "bias", "d", "epsilon", "u", "Timestamp_Python"])
    print(f"\nArchivo inicializado: {FULL_PATH}")

def Save_CSV_Row(datos_sistema, params_rele):
    """
    Añade una fila de datos al CSV (Referencia 1_Steps_Response).
    datos_sistema: [t_actual, angulo, error]
    params_rele: [bias, d, epsilon]
    """
    with open(FULL_PATH, mode='a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        # Combinamos: [t, ref, ang, err, bias, d, eps, u, ts_python]
        fila = [
            datos_sistema[0],  # t_s
            current_ref,       # ref
            datos_sistema[1],  # angulo
            datos_sistema[2],  # error
            params_rele[0],    # bias
            params_rele[1],    # d
            params_rele[2],    # epsilon
            current_u,         # u
            round(time.time(), 4) # Timestamp_Python
        ]
        writer.writerow(fila)

# --- CLASE DE COMUNICACIÓN ---

class ComunicacionESP32:
    def __init__(self, puerto):
        self.ser = serial.Serial(puerto, BAUD_RATE, timeout=0.1)
        self.angulo_actual = 0.0
        self.corriendo = True
        self.hilo = threading.Thread(target=self._leer_serial, daemon=True)
        self.hilo.start()

    def _leer_serial(self):
        while self.corriendo:
            try:
                linea = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if linea and ',' in linea:
                    partes = linea.split(',')
                    if len(partes) >= 2:
                        self.angulo_actual = float(partes[1])
            except: pass

    def enviar_pwm(self, u):
        self.ser.write(f"M:{u:.2f}\n".encode())

    def enviar_idle(self):
        self.ser.write(b"I\n")

    def enviar_calibracion(self):
        self.ser.write(b"CAL\n")

    def cerrar(self):
        self.corriendo = False
        self.ser.close()

def seleccionar_puerto():
    puertos = [p.device for p in serial.tools.list_ports.comports()]
    if not puertos:
        print("Error: No se detectaron puertos seriales."); sys.exit(1)
    print("\nPuertos detectados:")
    for i, p in enumerate(puertos): print(f"   [{i}] {p}")
    try:
        idx = int(input("\nSelecciona el índice del puerto: "))
        return puertos[idx]
    except:
        print("Selección inválida."); sys.exit(1)

def main():
    global current_u, current_ref
    puerto = seleccionar_puerto()
    esp = ComunicacionESP32(puerto)

    # --- CONFIGURACIÓN INICIAL ---
    print("\n" + "*"*60)
    respuesta = input("¿Desea calibrar el sensor? (CALIBRAR o Enter para saltar): ").strip().upper()
    if respuesta == "CALIBRAR":
        print("[SISTEMA] Calibrando... Espere.")
        esp.enviar_calibracion()
        time.sleep(2.0) 
    
    # Inicializar CSV usando la nueva lógica
    Initialize_CSV()
    
    est = {
        "ref": 15.0, "bias": 1.0, "d": 1.0, "epsilon": 3.0,
        "rele_alto": True, "corriendo": True, "motor_activo": True 
    }
    current_ref = est["ref"]

    cola_cmds = Queue()
    def hilo_input():
        while est["corriendo"]:
            linea = sys.stdin.readline().strip()
            if linea: cola_cmds.put(linea)
    threading.Thread(target=hilo_input, daemon=True).start()

    print("\n" + "="*90)
    print(" EXPERIMENTO MÉTODO DEL RELÉ - HELICÓPTERO 1-DOF")
    print(" COMANDOS: ref <v> | bias <v> | d <v> | eps <v> | i (idle) | q (salir)")
    print("="*90 + "\n")

    t_inicio = time.time()
    t_ultimo_print = 0

    try:
        while est["corriendo"]:
            t_ciclo = time.time()
            
            # 1. Procesar Comandos
            try:
                cmd_raw = cola_cmds.get_nowait()
                partes = cmd_raw.lower().split()
                if partes:
                    cmd = partes[0]
                    if cmd == 'q': est["corriendo"] = False
                    elif cmd == 'i':
                        est["motor_activo"] = False
                        esp.enviar_idle()
                        sys.stdout.write("\n!!! Interrupción detectada. Motor detenido.\n")
                    elif len(partes) > 1:
                        val = float(partes[1])
                        key = "epsilon" if cmd == "eps" else cmd
                        if key in est:
                            est[key] = val
                            if key == "ref": current_ref = val
                            est["motor_activo"] = True 
                            sys.stdout.write(f"\n[OK] {cmd.upper()} -> {val}\n")
            except (Empty, ValueError): pass

            # 2. Lógica de Control Relé
            angulo = esp.angulo_actual
            error = est["ref"] - angulo
            
            if est["motor_activo"]:
                if error > est["epsilon"]:
                    est["rele_alto"] = True
                elif error < -est["epsilon"]:
                    est["rele_alto"] = False
                
                current_u = est["bias"] + (est["d"] if est["rele_alto"] else -est["d"])
                current_u = max(U_MIN, min(U_MAX, current_u))
                esp.enviar_pwm(current_u)
            else:
                current_u = 0.0

            # 3. Guardar Datos usando la nueva lógica Save_CSV_Row
            t_actual = round(time.time() - t_inicio, 3)
            Save_CSV_Row(
                [t_actual, round(angulo, 2), round(error, 2)],
                [est["bias"], est["d"], est["epsilon"]]
            )

            # 4. Telemetría
            if t_actual - t_ultimo_print >= 0.5:
                status = "ACTV" if est["motor_activo"] else "IDLE"
                telemetria = (
                    f"\r\033[K[{status}] "
                    f"T:{t_actual:5.1f}s | Ref:{est['ref']:4.1f}° | Ang:{angulo:5.2f}° | "
                    f"Err:{error:5.2f} | B:{est['bias']:4.1f} | Eps:{est['epsilon']:3.1f} | "
                    f"d:{est['d']:4.1f} | U:{current_u:4.1f}% >> "
                )
                sys.stdout.write(telemetria)
                sys.stdout.flush()
                t_ultimo_print = t_actual

            time.sleep(max(0, DT_CONTROL - (time.time() - t_ciclo)))

    finally:
        print("\n\n[FINALIZANDO] Sistema cerrado.")
        esp.enviar_idle()
        esp.cerrar()

if __name__ == "__main__":
    main()