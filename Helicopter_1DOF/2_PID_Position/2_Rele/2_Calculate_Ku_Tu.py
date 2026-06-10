"""
Results_Relay.py - Analizador de sintonía automática (Relé).
Modificado para calcular parámetros PID (Ti, Td) y ganancias (Ki, Kd).
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
GRAFICAS_DIR = os.path.join(BASE_DIR, "Results")
CSV_KU_TU_RESUMEN = os.path.join(BASE_DIR, "Results", "ku_tu_por_referencia.csv")

Path(GRAFICAS_DIR).mkdir(exist_ok=True)

def a_float(valor: str, default=0.0):
    try:
        if valor is None or str(valor).strip() == "":
            return default
        return float(valor)
    except (ValueError, TypeError):
        return default

def cargar_datos_completos(ruta: str) -> dict:
    datos = {
        "t": [], "ref": [], "angulo": [],
        "error": [], "u": [], "d": [], "epsilon": []
    }
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró: {ruta}")

    with open(ruta, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            datos["t"].append(a_float(fila.get("t_s")))
            datos["ref"].append(a_float(fila.get("ref")))
            datos["angulo"].append(a_float(fila.get("angulo")))
            datos["error"].append(a_float(fila.get("error")))
            datos["u"].append(a_float(fila.get("u")))
            datos["d"].append(a_float(fila.get("d")))
            datos["epsilon"].append(a_float(fila.get("epsilon")))
    return datos

def calcular_parametros_ku(datos_util: dict) -> dict:
    error = np.array(datos_util["error"], dtype=float)
    if error.size == 0:
        return {"a": 0.0, "d": 0.0, "epsilon": 0.0, "ku": 0.0}

    amplitud_a = float((np.percentile(error, 95) - np.percentile(error, 5)) / 2.0)
    d = float(np.median(datos_util["d"]))
    epsilon = float(np.median(datos_util["epsilon"]))

    termino = amplitud_a**2 - epsilon**2
    if termino <= 0 or d <= 0:
        ku = 0.0
    else:
        ku = (4.0 * d) / (np.pi * np.sqrt(termino))
    
    return {"a": amplitud_a, "d": d, "epsilon": epsilon, "ku": ku}

def detectar_cruces_cero(error: list, t: list) -> list:
    cruces = []
    for i in range(1, len(error)):
        if error[i - 1] * error[i] < 0:
            peso = abs(error[i - 1]) / (abs(error[i - 1]) + abs(error[i]))
            t_cruce = t[i - 1] + peso * (t[i] - t[i - 1])
            cruces.append({"idx": i, "t": t_cruce})
    return cruces

def detectar_tramo_oscilacion_estable(error: list, t: list, num_oscilaciones: int = 10, 
                                      tolerance_periodo: float = 0.15) -> dict | None:
    cruces = detectar_cruces_cero(error, t)
    if len(cruces) < num_oscilaciones * 2:
        return None

    periodos = []
    for i in range(1, len(cruces)):
        periodos.append(2 * (cruces[i]["t"] - cruces[i - 1]["t"]))

    mejor_tramo = None
    min_varianza = float("inf")
    n_periodos_ventana = num_oscilaciones * 2
    for i in range(len(periodos) - n_periodos_ventana):
        ventana = periodos[i : i + n_periodos_ventana]
        avg = np.mean(ventana)
        std = np.std(ventana)
        if avg > 0 and (std / avg) < tolerance_periodo:
            if std < min_varianza:
                min_varianza = std
                idx_ini = cruces[i]["idx"]
                idx_fin = cruces[i + n_periodos_ventana]["idx"]
                mejor_tramo = {
                    "idx_inicio": idx_ini, "idx_final": idx_fin,
                    "t_inicio": t[idx_ini], "t_final": t[idx_fin],
                    "periodo_promedio": avg, "periodo_std": std
                }
    return mejor_tramo

def calcular_pid_zn(ku: float, tu: float) -> dict:
    """Calcula parámetros Ti, Td y ganancias Ki, Kd según Ziegler-Nichols."""
    if ku <= 0 or tu <= 0:
        return {"kp": 0, "ti": 0, "td": 0, "ki": 0, "kd": 0}
    
    # 1. Parámetros de la Tabla (Forma Estándar)
    kp = 0.6 * ku
    ti = tu / 2.0
    td = tu / 8.0
    
    # 2. Conversión a Ganancias de Implementación (Forma Paralela)
    ki = kp / ti if ti > 0 else 0
    kd = kp * td
    
    return {"kp": kp, "ti": ti, "td": td, "ki": ki, "kd": kd}

def procesar_archivo(ruta: str) -> dict:
    datos = cargar_datos_completos(ruta)
    tramo = detectar_tramo_oscilacion_estable(datos["error"], datos["t"])
    if tramo is None:
        raise ValueError("No se encontró un tramo de oscilaciones estable.")

    idx_i, idx_f = tramo["idx_inicio"], tramo["idx_final"]
    datos_util = {k: v[idx_i:idx_f] for k, v in datos.items()}
    
    pk = calcular_parametros_ku(datos_util)
    pid = calcular_pid_zn(pk["ku"], tramo["periodo_promedio"])
    ref_val = np.median(datos["ref"])

    return {
        "completo": datos, "util": datos_util, "tramo_estable": tramo,
        "params_ku": pk, "pid": pid, "referencia": ref_val, "nombre": os.path.basename(ruta)
    }

def crear_grafica_analisis(res: dict, path_save: str):
    fig, axs = plt.subplots(3, 1, figsize=(12, 11), sharex=True)
    d_all, tr, pk, pid = res["completo"], res["tramo_estable"], res["params_ku"], res["pid"]

    axs[0].plot(d_all["t"], d_all["ref"], 'r--', label="Referencia")
    axs[0].plot(d_all["t"], d_all["angulo"], 'b-', label="Ángulo Real")
    axs[0].axvspan(tr["t_inicio"], tr["t_final"], color='yellow', alpha=0.2, label="Tramo Estable")
    axs[0].set_ylabel("Ángulo (°)")
    axs[0].legend(loc="upper right"); axs[0].grid(True, alpha=0.3)

    axs[1].plot(d_all["t"], d_all["error"], color='orange', label="Error")
    axs[1].axhline(0, color='black', lw=1); axs[1].set_ylabel("Error (°)"); axs[1].grid(True, alpha=0.3)

    axs[2].plot(d_all["t"], d_all["u"], color='green', label="PWM Control (u)")
    axs[2].set_ylabel("Control (%)"); axs[2].set_xlabel("Tiempo (s)"); axs[2].grid(True, alpha=0.3)

    res_txt = (f"IDENTIFICACIÓN:\nKu: {pk['ku']:.3f}\nTu: {tr['periodo_promedio']:.3f}s\n\n"
               f"SINTONÍA ZN:\nKp: {pid['kp']:.3f}\nTi: {pid['ti']:.3f}s\nTd: {pid['td']:.3f}s\n\n"
               f"PARA PYTHON:\nKi: {pid['ki']:.4f}\nKd: {pid['kd']:.4f}")
    
    fig.text(0.83, 0.15, res_txt, fontsize=9, family='monospace', 
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.9))

    plt.tight_layout(rect=[0, 0.05, 0.82, 0.95])
    plt.savefig(path_save, dpi=150); plt.close()

def main():
    archivos = sorted(glob.glob(CSV_PATTERN))
    if not archivos: return
    
    resultados_lista = []
    for ruta in archivos:
        try:
            res = procesar_archivo(ruta)
            graf_path = os.path.join(GRAFICAS_DIR, f"Analisis_Ref{res['referencia']:.0f}.png")
            crear_grafica_analisis(res, graf_path)

            resultados_lista.append({
                "Ref_deg": res["referencia"],
                "Ku": round(res["params_ku"]["ku"], 4),
                "Tu_s": round(res["tramo_estable"]["periodo_promedio"], 4),
                "Kp": round(res["pid"]["kp"], 4),
                "Ti_s": round(res["pid"]["ti"], 4),
                "Td_s": round(res["pid"]["td"], 4),
                "Ki": round(res["pid"]["ki"], 5),
                "Kd": round(res["pid"]["kd"], 5)
            })
            print(f"Ref {res['referencia']}: Kp={res['pid']['kp']:.2f}, Ki={res['pid']['ki']:.4f}, Kd={res['pid']['kd']:.4f}")
        except Exception as e:
            print(f"Error en {ruta}: {e}")

    if resultados_lista:
        with open(CSV_KU_TU_RESUMEN, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=resultados_lista[0].keys())
            w.writeheader()
            w.writerows(resultados_lista)
        print(f"\nResultados PID guardados en: {CSV_KU_TU_RESUMEN}")

if __name__ == "__main__":
    main()