%% PROGRAMA DE DEMOSTRACIÓN EN CLASE: De un solo tramo

clear; close all; clc; 

%% Definir las variables necesarias: 
q0  = 0;         % posición inicial
qf  = 10;        % posición final
qd_max  = 4;   % Velocidad máxima (rad/s)
T_tot = 4;       % tiempo en segundos que debería durar la trayectoria (s)

t = linspace(0, T_tot, 1000);% Vector para simular el tiempo

%% Condición de validez
fprintf("El tiempo de trayectoria debe ser: \n T_total > %.4f  \n T_total < %4.f\n\n", (qf-q0)/qd_max, 2*(qf-q0)/qd_max);

if (T_tot>(qf-q0)/qd_max && T_tot<(2*(qf-q0)/qd_max))
    fprintf("Condición válida\n");
else
    fprintf("Condición NO válida\n");
    return;
end

%% Se calcula los tiempos de cada tramo, como la aceleración máxima
tao1 = T_tot - (qf-q0)/qd_max;  % Tiempo de tramo 1
tao2 = T_tot -2*tao1;       % Tiempo del tramo 2 
tao3 = tao1;                % Tiempo del tramo 3

qdd_max  = qd_max/tao1;             % Aceleración máxima

%% Inicializar los vectores de aceleración, velocidad y posición
vec_qdd = zeros(1, length(t)); 
vec_qd  = zeros(1, length(t)); 
vec_q   = zeros(1, length(t)); 


%% Crear la función de velocidad discontinua de tiempo 
for i = 1:length(t)
    ti = t(i);

    if ti <= tao1
        % Tramo 1: Aceleración constante
        vec_qdd(i) = qdd_max;                   % Aceleración constante en este tramo
        vec_qd(i)  = qdd_max*ti;                % Tramo lineal de velocidad 
        vec_q(i)   = q0 + 0.5*vec_qdd(i)*ti^2;  % Posición parabólica

    elseif ti <= tao1+tao2
        % Tramo 2: Aceleración 0
        vec_qdd(i) = 0; 
        vec_qd(i)  = qd_max;
        vec_q(i)   = q0+0.5*qd_max*tao1+ qd_max*(ti-tao1);
    else
        % Tramo 3: Desaceleración
        dt= ti-(tao1+tao2);
        vec_qdd(i) = -qdd_max;
        vec_qd(i)  = qd_max-qdd_max*dt; 
        vec_q(i)   = q0+  0.5*qd_max*tao1+  qd_max*tao2+  qd_max*dt-  0.5*qdd_max*(dt)^2;
    end
end

% Armar la entrada al controlador
ref = [t; vec_qd]';


% --- Posición angular ---
subplot(3, 1, 1);
plot(t, vec_q, 'b-', 'LineWidth', 2);
hold on;
ylabel('\theta (rad)');
title('QUBE Servo 3 - Trayectoria Trapezoidal');
legend('Posición angular');
grid on;

subplot(3, 1, 2);
plot(t, vec_qd, "LineWidth", 2);
hold on;
ylabel("Velocidad  (rad/s)");
legend("Velocidad")
grid on; 

subplot(3, 1, 3)
plot(t, vec_qdd, "Linewidth", 2);
hold on; 
ylabel("Aceleración");
legend("Aceleración");
grid on; 

% Nota: Para tramos de desaceleración o cambios de giro, se debe utilizar
% la función signo y la magnitud. 