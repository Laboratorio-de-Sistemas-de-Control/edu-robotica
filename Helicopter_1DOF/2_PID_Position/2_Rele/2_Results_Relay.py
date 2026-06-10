"""
Results_Relay_Manual.py - Visualizador interactivo para sintonía manual.
Muestra la respuesta angular y la señal de control en ventanas emergentes.
"""

import csv
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATTERN = os.path.join(BASE_DIR, "Results", "2_results_rele.csv")

def a_float(valor, default=0.0):
    try:
        if valor is None or str(valor).strip() == "":
            return default
        return float(valor)
    except (ValueError, TypeError):
        return default

def cargar_datos(ruta: str) -> dict:
    datos = {"t": [], "ref": [], "angulo": [], "u": []}
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    with open(ruta, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            datos["t"].append(a_float(fila.get("t_s")))
            datos["ref"].append(a_float(fila.get("ref")))
            datos["angulo"].append(a_float(fila.get("angulo")))
            datos["u"].append(a_float(fila.get("u")))
    return datos

def mostrar_grafica_estudiante(datos, ref_valor, nombre_archivo):
    # Creamos 2 subplots: Posición y Señal de Control
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    fig.suptitle(f"Análisis de Relé - Archivo: {nombre_archivo}\nReferencia: {ref_valor}°", 
                 fontsize=14, fontweight='bold')

    # Gráfica de Posición Angular
    ax1.plot(datos["t"], datos["ref"], 'r--', alpha=0.8, label="Referencia (Set-point)")
    ax1.plot(datos["t"], datos["angulo"], 'b-', lw=1.2, label="Posición Angular (°)")
    ax1.set_ylabel("Ángulo (°)")
    ax1.set_title("Respuesta del Sistema (Variable de Proceso)")
    ax1.legend(loc="upper right")
    ax1.grid(True, which='both', linestyle='--', alpha=0.5)

    # Gráfica de Señal de Control (PWM)
    ax2.step(datos["t"], datos["u"], color='green', where='post', lw=1.2, label="Señal de Control (u)")
    ax2.set_ylabel("PWM (%)")
    ax2.set_xlabel("Tiempo (s)")
    ax2.set_title("Salida del Relé (Variable Manipulada)")
    ax2.legend(loc="upper right")
    ax2.grid(True, which='both', linestyle='--', alpha=0.5)

    # Ajuste de diseño
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Muestra la ventana interactiva (permite hacer zoom para medir amplitudes y periodos)
    print(f"  [INFO] Mostrando gráfica. Cierra la ventana para continuar.")
    plt.show()

def main():
    # Buscar archivos
    archivos = sorted(glob.glob(CSV_PATTERN))
    if not archivos:
        print(f"No se encontraron archivos CSV en la ruta: {CSV_PATTERN}")
        return

    for ruta in archivos:
        try:
            nombre_archivo = os.path.basename(ruta)
            print(f"Leyendo: {nombre_archivo}...")
            
            datos = cargar_datos(ruta)
            
            if not datos["t"]:
                print(f"  [!] El archivo {nombre_archivo} está vacío.")
                continue

            ref_valor = np.median(datos["ref"])
            
            # Llamada a mostrar en lugar de guardar
            mostrar_grafica_estudiante(datos, ref_valor, nombre_archivo)

        except Exception as e:
            print(f"  [ERROR] No se pudo procesar {ruta}: {e}")

if __name__ == "__main__":
    main()