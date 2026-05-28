%% Trayectoria Lineal de Posición
% Programa que calcula una trayectoria lineal entre dos configuraciones
% articulares y genera una matriz con tiempo, posición y velocidad

clear all; close all; clc;

%% Parámetros de la trayectoria
t0 = 0;      % Tiempo inicial [s]
tf = 5;      % Tiempo final [s]
q0 = 0;      % Posición inicial [rad]
qf = 100;    % Posición final [rad]

%% Calcular coeficientes a1 y a0
% Sistema de ecuaciones matricial: A * x = b
% [t0  1] [a1]   [q0]
% [tf  1] [a0] = [qf]

A = [t0, 1;
     tf, 1];
b = [q0; qf];

x = A \ b;  % Solución: x = A^(-1) * b
a1 = x(1);  % Pendiente (velocidad constante)
a0 = x(2);  % Término independiente

fprintf('=== TRAYECTORIA LINEAL DE POSICIÓN ===\n');
fprintf('Condiciones de frontera:\n');
fprintf('  Posición inicial: q0 = %.4f rad en t0 = %.2f s\n', q0, t0);
fprintf('Posición final:   qf = %.4f rad en tf = %.2f s\n', qf, tf);
fprintf('\nCoeficientes calculados:\n');
fprintf('  Pendiente (a1):  %.4f rad/s\n', a1);
fprintf('  Término indep. (a0): %.4f rad\n', a0);
fprintf('\nEcuación de la trayectoria:\n');
fprintf('  q(t) = %.4f * t + %.4f\n', a1, a0);

%% Generar vector de tiempo
dt = 0.1;         % Incremento de tiempo [s]
t = (t0:dt:tf)';  % Vector de tiempo (columna)

%% Calcular posición y velocidad para cada instante
n = length(t);
q = a1 * t + a0;        % Posición articular
vel = a1 * ones(n, 1);  % Velocidad (constante)
acel = zeros(n, 1);     % Aceleración (nula)

%% Crear matriz de resultados
% Columnas: tiempo, posición, velocidad, aceleración
trayectoria = [t, q, vel, acel];
referencia_ctrl = [t, vel];

%% Mostrar resultados
fprintf('\n=== MATRIZ DE TRAYECTORIA ===\n');
fprintf('Columnas: [tiempo, posición, velocidad, aceleración]\n\n');
disp(trayectoria);

%% Gráficas
figure('Name', 'Trayectoria Lineal de Posición', 'NumberTitle', 'off');

% Gráfica de posición
subplot(3,1,1);
plot(t, q, 'b-', 'LineWidth', 2);
grid on; xlabel('Tiempo [s]'); ylabel('Posición [rad]');
title('Posición Articular q(t)');
ylim([q0-0.5, qf+0.5]);

% Gráfica de velocidad
subplot(3,1,2);
plot(t, vel, 'g-', 'LineWidth', 2);
grid on; xlabel('Tiempo [s]'); ylabel('Velocidad [rad/s]');
title('Velocidad Articular \\dot{q}(t)');
ylim([a1-0.2, a1+0.2]);

% Gráfica de aceleración
subplot(3,1,3);
plot(t, acel, 'r-', 'LineWidth', 2);
grid on; xlabel('Tiempo [s]'); ylabel('Aceleración [rad/s²]');
title('Aceleración Articular \\ddot{q}(t)');
ylim([-0.1, 0.1]);
