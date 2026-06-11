# edu-robotica

Material de prácticas para la asignatura de **Robótica** — Maestría en Ciencias de la Ingeniería Eléctrica, Universidad de Cuenca.

La guía completa de prácticas se encuentra en [`Manual_Prácticas_Robótica.pdf`](Manual_Prácticas_Robótica.pdf).

## Contenido

El repositorio incluye material para cinco prácticas presenciales:

### Práctica 1 — Control de velocidad con el QUBE-Servo 3
Identificación experimental del modelo dinámico del motor DC mediante respuesta al escalón en lazo abierto. Implementación y comparación de controladores P y PI, finalizando con la sintonización experimental de un controlador PID.

### Práctica 2 — Control de posición con el QUBE-Servo 3
Control de posición angular del disco de inercia. Se implementan controladores P y PD (usando la velocidad angular medida en la rama derivativa), y como reto se sintoniza un controlador PID completo.

### Práctica 3 — Control de posición para helicóptero de 1 DOF
Sistema no lineal controlado desde Python vía comunicación serial con un ESP32 S3. Se sintoniza un PID local mediante el método del relé (Åström-Hägglund) y como reto se implementa un esquema de **Gain Scheduling** para cubrir el rango operativo completo (0°–65°).

### Práctica 4 — Planificación de trayectorias para el QUBE-Servo 3
Estudio e implementación de tres familias de perfiles cinemáticos de complejidad creciente: trayectoria de velocidad constante, trapezoidal y una trayectoria adicional de libre elección (por ejemplo, mínimo jerk mediante `minjerkpolytraj` o `contopptraj`). Los perfiles se generan en MATLAB, se analizan sus características cinemáticas (posición, velocidad, aceleración y jerk) y se validan experimentalmente sobre el QUBE-Servo 3 mediante un controlador de velocidad en Simulink.

### Práctica 5 — Control del péndulo invertido
Estabilización del péndulo rotatorio invertido montado sobre el QUBE-Servo 3 mediante un esquema de control híbrido. Se diseña un regulador óptimo **LQR** (*Linear Quadratic Regulator*) para estabilizar el péndulo en la posición vertical inestable, y se integra con un algoritmo de balanceo inicial **Swing Up** basado en inyección de energía. La lógica de conmutación entre ambos controladores se implementa en Simulink y se valida en tiempo real sobre el hardware.

## Equipos

| Equipo | Prácticas |
|--------|-----------|
| QUBE-Servo 3 (Quanser) | 1, 2, 4 y 5 |
| Helicóptero 1-DOF + ESP32 S3 + IMU GY-86 | 3 |

## Herramientas

- MATLAB/Simulink + QUARC (Prácticas 1, 2, 4 y 5)
- Python + Arduino IDE (Práctica 3)