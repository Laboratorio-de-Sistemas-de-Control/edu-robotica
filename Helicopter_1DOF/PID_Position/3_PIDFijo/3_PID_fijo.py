from __future__ import annotations

import csv
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from queue import Empty, Queue

from utils import BAUD_RATE, PuertoHelicoptero, seleccionar_puerto

# --- CONFIGURACIÓN ---
BAUD_RATE = 115200
DT_CONTROL = 0.01
FREQ_MS = max(10, min(500, int(DT_CONTROL * 1000)))
PRINT_EVERY_S = 0.25
REF_MIN = 0.0
REF_MAX = 45.0
U_MIN = 0.0
U_MAX = 60.0

BASE_DIR = Path(__file__).resolve().parent
CSV_LOG = BASE_DIR / "pid_estudiantes_log.csv"

@dataclass(slots=True)
class Ganancias:
    kp: float
    ki: float
    kd: float

@dataclass(slots=True)
class EstadoControl:
    setpoint: float = 0.0
    u: float = 0.0
    e1: float = 0.0
    e2: float = 0.0
    activo: bool = False
    pendiente_sincronizar_error: bool = False

    def reset(self) -> None:
        self.u = 0.0
        self.e1 = 0.0
        self.e2 = 0.0

# ==========================================================
# SECCIÓN PARA ESTUDIANTES: CÁLCULO DE CONTROL
# ==========================================================
def control_PID(ref_actual: float) -> Ganancias:
    """
    Función para que los estudiantes coloquen sus ganancias.
    Pueden ser fijas o pueden implementar una lógica de selección aquí.
    """
    # Ejemplo: Los estudiantes deben modificar estos valores
    # calculados con el método del relé para su referencia elegida.

    kp = 1.043
    ki = 1.7158
    kd = 0.1584
    
    return Ganancias(kp=kp, ki=ki, kd=kd)

def calcular_control(
    setpoint: float,
    angulo: float,
    estado: EstadoControl,
    dt: float = DT_CONTROL,
) -> tuple[float, float, Ganancias]:
    
    # Obtener ganancias desde la función de los estudiantes
    ganancias = control_PID(setpoint)
    
    # Error actual
    e_k = setpoint - angulo

    # Ecuación de control PID (Forma recursiva/velocidad)
    # u[k] = u[k-1] + Kp*(e[k]-e[k-1]) + Ki*dt*e[k] + (Kd/dt)*(e[k]-2e[k-1]+e[k-2])
    term_p = ganancias.kp * (e_k - estado.e1)
    term_i = (ganancias.ki * dt) * e_k
    term_d = (ganancias.kd / dt) * (e_k - 2.0 * estado.e1 + estado.e2)

    u_new = estado.u + term_p + term_i + term_d
    
    # Saturación de la salida
    u_new = max(U_MIN, min(U_MAX, u_new))

    # Actualización de estados para el siguiente ciclo
    estado.u = u_new
    estado.e2 = estado.e1
    estado.e1 = e_k

    return e_k, u_new, ganancias
# ==========================================================

def preguntar_y_n(mensaje: str) -> bool:
    while True:
        resp = input(f"{mensaje} (Y/N): ").strip().upper()
        if resp == "Y": return True
        if resp == "N": return False
        print("  Respuesta invalida. Use solo Y o N.")

def pedir_referencia_inicial() -> float:
    while True:
        entrada = input(f"Referencia inicial [{REF_MIN}-{REF_MAX}] deg (default 0): ").strip()
        if entrada == "": return 0.0
        try:
            valor = float(entrada)
            if REF_MIN <= valor <= REF_MAX: return valor
            print(f"  Fuera de rango.")
        except ValueError:
            print("  Ingresa un numero valido.")

def iniciar_hilo_comandos() -> Queue[str]:
    cola: Queue[str] = Queue()
    def lector() -> None:
        while True:
            try:
                linea = sys.stdin.readline().strip()
                if linea: cola.put(linea)
            except EOFError: break
    threading.Thread(target=lector, daemon=True).start()
    return cola

def procesar_comando(cmd: str, estado: EstadoControl, enlace: PuertoHelicoptero) -> str:
    partes = cmd.split()
    if not partes: return "continuar"
    op = partes[0].lower()

    if op == "q": return "salir"
    if op == "start":
        estado.activo = True
        estado.pendiente_sincronizar_error = True
        print("\nControl iniciado.")
    elif op == "stop":
        estado.activo = False
        estado.reset()
        enlace.enviar_idle()
        print("\nControl detenido. Motor en IDLE.")
    elif op == "ref" and len(partes) == 2:
        try:
            ref = float(partes[1])
            if REF_MIN <= ref <= REF_MAX:
                estado.setpoint = ref
                estado.pendiente_sincronizar_error = True
                print(f"\nNueva referencia: {estado.setpoint:.2f} deg")
            else:
                print(f"\nReferencia fuera de rango.")
        except ValueError:
            print("\nValor no numerico.")
    return "continuar"

def main() -> None:
    print("--- PROGRAMA DE CONTROL PID (VERSIÓN ESTUDIANTES) ---")
    
    puerto = sys.argv[1] if len(sys.argv) > 1 else seleccionar_puerto()
    if not preguntar_y_n(f"¿Conectar a {puerto}?"): return

    try:
        enlace = PuertoHelicoptero.abrir(puerto, BAUD_RATE, timeout=1)
        enlace.configurar_frecuencia(FREQ_MS)
        enlace.enviar_idle()
        
        if preguntar_y_n("¿Requiere calibración de ESC?"):
            enlace.calibrar_esc()
            print("Calibrando... espere.")
            time.sleep(4) 
            enlace.enviar_idle()

        estado = EstadoControl(setpoint=pedir_referencia_inicial(), activo=False)
        comandos = iniciar_hilo_comandos()
        registros = []
        t0 = time.time()
        t_print = -1.0

        print("\nComandos: start, stop, ref <valor>, q (salir)")

        while True:
            ciclo_ini = time.time()
            
            # 1. Procesar Comandos de Usuario
            try:
                while True:
                    if procesar_comando(comandos.get_nowait(), estado, enlace) == "salir":
                        return
            except Empty: pass

            # 2. Leer Telemetría
            muestra = enlace.esperar_muestra(timeout=0.1)
            if muestra is None: continue

            # 3. Calcular Control
            if estado.activo:
                if estado.pendiente_sincronizar_error:
                    # Evitar salto integral/derivativo brusco al arrancar o cambiar ref
                    e_init = estado.setpoint - muestra.angulo
                    estado.e1 = estado.e2 = e_init
                    estado.pendiente_sincronizar_error = False
                
                err, u_cmd, g = calcular_control(estado.setpoint, muestra.angulo, estado)
                enlace.enviar_pwm(u_cmd)
            else:
                err, u_cmd = estado.setpoint - muestra.angulo, 0.0
                g = control_PID(estado.setpoint)

            # 4. Registro y Consola
            t_abs = time.time() - t0
            registros.append({
                "t_pc_s": round(t_abs, 3), "setpoint": estado.setpoint, 
                "angulo": muestra.angulo, "u": u_cmd, "kp": g.kp, "ki": g.ki, "kd": g.kd
            })

            if (t_abs - t_print) >= PRINT_EVERY_S:
                t_print = t_abs
                print(f"\r[{'ON' if estado.activo else 'OFF'}] Ref:{estado.setpoint:4.1f} | Ang:{muestra.angulo:5.1f} | U:{u_cmd:4.1f}%", end="")

            # Mantener frecuencia
            time.sleep(max(0, DT_CONTROL - (time.time() - ciclo_ini)))

    except KeyboardInterrupt: pass
    finally:
        if 'enlace' in locals():
            enlace.enviar_idle()
            enlace.cerrar()
        print(f"\nSesión terminada. Datos guardados en {CSV_LOG}")

if __name__ == "__main__":
    main()