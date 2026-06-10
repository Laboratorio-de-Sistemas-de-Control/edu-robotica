from __future__ import annotations

import sys
import threading
from dataclasses import dataclass
from queue import Empty, Queue

import serial
import serial.tools.list_ports

BAUD_RATE = 115200

@dataclass(slots=True)
class Telemetria:
    t_ms: int = 0
    angulo: float = 0.0
    pwm_pct: float = 0.0
    modo: str = "---"


class PuertoHelicoptero:
    """Encapsula la comunicacion serial, telemetria y mensajes del ESP32."""

    def __init__(self, ser: serial.Serial) -> None:
        self.ser = ser
        self._estado = Telemetria()
        self._lock = threading.Lock()
        self._listo = threading.Event()
        self._muestra_nueva = threading.Event()
        self._mensajes: Queue[str] = Queue()
        self._hilo = threading.Thread(target=self._hilo_lector, daemon=True)
        self._hilo.start()

    @classmethod
    def abrir(cls, puerto: str, baud_rate: int = BAUD_RATE, timeout: float = 1.0) -> "PuertoHelicoptero":
        return cls(serial.Serial(puerto, baud_rate, timeout=timeout))

    def _hilo_lector(self) -> None:
        while True:
            try:
                linea = self.ser.readline().decode("utf-8", errors="ignore").strip()
            except Exception:
                break

            if not linea:
                continue

            if linea == "LISTO":
                self._listo.set()
                self._mensajes.put(linea)
                continue

            partes = linea.split(",")
            if len(partes) != 4:
                self._mensajes.put(linea)
                continue

            try:
                muestra = Telemetria(
                    t_ms=int(partes[0]),
                    angulo=float(partes[1]),
                    pwm_pct=float(partes[2]),
                    modo=partes[3],
                )
            except ValueError:
                continue

            with self._lock:
                self._estado = muestra
            self._muestra_nueva.set()

    def esperar_listo(self, timeout: float = 8.0) -> bool:
        return self._listo.wait(timeout=timeout)

    def esperar_muestra(self, timeout: float = 0.5) -> Telemetria | None:
        self._muestra_nueva.clear()
        if not self._muestra_nueva.wait(timeout=timeout):
            return None
        return self.leer_estado()

    def leer_estado(self) -> Telemetria:
        with self._lock:
            return Telemetria(
                t_ms=self._estado.t_ms,
                angulo=self._estado.angulo,
                pwm_pct=self._estado.pwm_pct,
                modo=self._estado.modo,
            )

    def leer_mensajes(self) -> list[str]:
        mensajes: list[str] = []
        while True:
            try:
                mensajes.append(self._mensajes.get_nowait())
            except Empty:
                break
        return mensajes

    def enviar_pwm(self, pct: float) -> None:
        self.ser.write(f"M:{pct:.2f}\n".encode())

    def enviar_idle(self) -> None:
        self.ser.write(b"I\n")

    def calibrar_esc(self) -> None:
        self.ser.write(b"CAL\n")

    def configurar_frecuencia(self, periodo_ms: int) -> None:
        self.ser.write(f"FREQ:{periodo_ms}\n".encode())

    def cerrar(self) -> None:
        try:
            self.ser.close()
        except Exception:
            pass


def seleccionar_puerto() -> str:
    puertos = [p.device for p in serial.tools.list_ports.comports()]
    if not puertos:
        print("No se encontraron puertos seriales.")
        sys.exit(1)

    print("\nPuertos disponibles:")
    for i, puerto in enumerate(puertos):
        print(f"  [{i}]  {puerto}")

    while True:
        entrada = input("Selecciona el numero de puerto: ").strip()
        if entrada.isdigit() and int(entrada) < len(puertos):
            return puertos[int(entrada)]
        if entrada in puertos:
            return entrada
        print("  Opcion no valida.")
