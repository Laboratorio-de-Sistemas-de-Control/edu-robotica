import pandas as pd
import matplotlib.pyplot as plt
import os

# --- CONFIGURACIÓN DE RUTA ---
FOLDER_NAME = "Results"
FILE_NAME = "telemetria.csv"

# Construimos la ruta dinámica para encontrar la carpeta 'Results'
# al mismo nivel que este script.
BASE_DIR = os.path.dirname(__file__)
FULL_PATH = os.path.join(BASE_DIR, FOLDER_NAME, FILE_NAME)

def plot_data():
    # Verificar si el archivo existe en la ruta especificada
    if not os.path.exists(FULL_PATH):
        print(f"Error: No se encuentra el archivo en {FULL_PATH}")
        print("Asegúrate de haber ejecutado primero el programa de comunicación.")
        return

    try:
        # Leer el CSV
        df = pd.read_csv(FULL_PATH)

        if df.empty:
            print("El archivo está vacío. No hay datos para graficar.")
            return

        # Crear la figura con dos subgráficas (Ángulo y PWM)
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 7))

        # Gráfica 1: Ángulo
        ax1.plot(df['Timestamp_MS'], df['Angulo'], color='blue', linewidth=1.5, label='Ángulo (deg)')
        ax1.set_ylabel('Grados (°)')
        ax1.set_title('Telemetría: Ángulo vs Tiempo')
        ax1.legend(loc='upper right')
        ax1.grid(True, linestyle='--', alpha=0.7)

        # Gráfica 2: PWM
        ax2.plot(df['Timestamp_MS'], df['PWM'], color='red', linewidth=1.5, label='PWM (%)')
        ax2.set_ylabel('Ciclo de Trabajo (%)')
        ax2.set_xlabel('Tiempo (ms)')
        ax2.set_title('Telemetría: PWM vs Tiempo')
        ax2.legend(loc='upper right')
        ax2.grid(True, linestyle='--', alpha=0.7)

        plt.suptitle(f'Resultados desde: {FOLDER_NAME}/{FILE_NAME}', fontsize=12)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Ocurrió un error al procesar los datos: {e}")

if __name__ == "__main__":
    plot_data()