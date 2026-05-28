# edu-robotica

Material de prácticas para la asignatura de **Robótica** — Maestría en Ciencias de la Ingeniería Eléctrica, Universidad de Cuenca.

La guía completa de prácticas se encuentra en [`Manual_Prácticas_Robótica.pdf`](Manual_Prácticas_Robótica.pdf).

## Contenido

El repositorio incluye material para tres prácticas presenciales:

### Práctica 1 — Control de velocidad con el QUBE-Servo 3
Identificación experimental del modelo dinámico del motor DC mediante respuesta al escalón en lazo abierto. Implementación y comparación de controladores P y PI, finalizando con la sintonización experimental de un controlador PID.

### Práctica 2 — Control de posición con el QUBE-Servo 3
Control de posición angular del disco de inercia. Se implementan controladores P y PD (usando la velocidad angular medida en la rama derivativa), y como reto se sintoniza un controlador PID completo.

### Práctica 3 — Control de posición para helicóptero de 1 DOF
Sistema no lineal controlado desde Python vía comunicación serial con un ESP32 S3. Se sintoniza un PID local mediante el método del relé (Åström-Hägglund) y como reto se implementa un esquema de **Gain Scheduling** para cubrir el rango operativo completo (0°–65°).

## Equipos

| Equipo | Prácticas |
|--------|-----------|
| QUBE-Servo 3 (Quanser) | 1 y 2 |
| Helicóptero 1-DOF + ESP32 S3 + IMU GY-86 | 3 |

## Herramientas

- MATLAB/Simulink + QUARC (Prácticas 1 y 2)
- Python + Arduino IDE (Práctica 3)

