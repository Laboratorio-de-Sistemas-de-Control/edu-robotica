"""
0_Results_Analysis.py — Visualización de Telemetría e Histéresis

Este script procesa los datos del experimento de escalones para mostrar:
  1. La respuesta temporal del ángulo frente a los cambios de potencia (Escalones).
  2. La curva de histéresis (Ángulo vs PWM) para comparar subida y bajada.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- CONFIGURACIÓN DE RUTA ---
FOLDER_NAME = "Results"
FILE_NAME = "1_results_steps_response.csv"
BASE_DIR = os.path.dirname(__file__)
FULL_PATH = os.path.join(BASE_DIR, FOLDER_NAME, FILE_NAME)

def plot_analysis():
    if not os.path.exists(FULL_PATH):
        print(f"Error: No se encuentra el archivo en {FULL_PATH}")
        return

    # Leer datos
    df = pd.read_csv(FULL_PATH)
    if df.empty:
        print("El archivo está vacío.")
        return

    # Convertir tiempo de ms a s para mejor lectura
    df['t_s'] = (df['Timestamp_MS'] - df['Timestamp_MS'].iloc[0]) / 1000.0

    # --- GRÁFICA 1: RESPUESTA TEMPORAL ---
    fig1, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 7))
    
    ax1.plot(df['t_s'], df['Angulo'], color='blue', label='Ángulo Medido [°]')
    ax1.set_ylabel('Grados (°)')
    ax1.set_title('Respuesta Temporal: Ángulo vs Tiempo')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()

    ax2.plot(df['t_s'], df['Escalon_Set'], color='red', label='Consigna PWM [%]')
    ax2.set_ylabel('Potencia (%)')
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_title('Entrada: Escalones de Potencia')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()
    
    plt.tight_layout()

    # --- GRÁFICA 2: HISTÉRESIS ---
    # Separamos los datos cuando el PWM sube y cuando baja
    # Buscamos el punto máximo de potencia para dividir el experimento
    idx_max_pwm = df['Escalon_Set'].idxmax()
    
    subida = df.iloc[:idx_max_pwm + 1]
    bajada = df.iloc[idx_max_pwm:]

    # Agrupamos por escalón para obtener el promedio en estado estable
    # (Esto limpia el ruido de la gráfica de histéresis)
    sub_avg = subida.groupby('Escalon_Set')['Angulo'].mean().reset_index()
    baj_avg = bajada.groupby('Escalon_Set')['Angulo'].mean().reset_index()

    plt.figure(figsize=(8, 6))
    plt.plot(sub_avg['Escalon_Set'], sub_avg['Angulo'], 'bo-', label='Trayectoria Subida')
    plt.plot(baj_avg['Escalon_Set'], baj_avg['Angulo'], 'ro-', label='Trayectoria Bajada')
    
    # Relleno del área de histéresis
    plt.fill_between(sub_avg['Escalon_Set'], 
                     sub_avg['Angulo'], 
                     baj_avg.set_index('Escalon_Set').reindex(sub_avg['Escalon_Set'])['Angulo'],
                     color='purple', alpha=0.1, label='Área de Histéresis')

    plt.title('Curva de Histéresis: Ángulo vs Potencia')
    plt.xlabel('Potencia PWM (%)')
    plt.ylabel('Ángulo de Equilibrio (°)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    plt.show()

if __name__ == "__main__":
    plot_analysis()