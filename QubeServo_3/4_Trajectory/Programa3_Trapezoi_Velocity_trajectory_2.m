%% PROGRAMA DE DEMOSTRACIÓN EN CLASE: De varios tramos

clear; close all; clc;

% TRAYECTORIA TRAPEZOIDAL MULTITRAMO
% puntos:
%   Define las posiciones que debe recorrer el sistema.
% velocidades:
%   Velocidad máxima permitida para cada tramo.
% tiempos:
%   Tiempo deseado para cada tramo.
% IMPORTANTE:
%   La cantidad de velocidades y tiempos debe ser:
%
%       length(puntos)-1
% porque cada tramo conecta dos puntos.


%% Datos de usuario
puntos      = [0 10 -60];
velocidades = [4 4];
tiempos     = [4 18];

%% Verificación de dimensiones
if length(velocidades) ~= length(puntos)-1
    error("Cantidad incorrecta de velocidades");
end

if length(tiempos) ~= length(puntos)-1
    error("Cantidad incorrecta de tiempos");
end

%% Variables de trayectoria
Q   = [];   % Posición
Qd  = [];   % Velocidad
Qdd = [];   % Aceleración
T   = [];   % Tiempo

tiempo_global = 0;

%% Generación de trayectoria
for i = 1:length(puntos)-1

    % Datos del tramo actual
    q0   = puntos(i);
    qf   = puntos(i+1);

    vmax = velocidades(i);
    Ttot = tiempos(i);

    % Distancia del tramo
    dist = abs(qf-q0);

    % Restricciones del perfil trapezoidal
    Tmin = dist/vmax;
    Tmax = 2*dist/vmax;

    % Verificación de factibilidad
    if Ttot <= Tmin || Ttot >= Tmax

        fprintf("\n----------------------------------\n");
        fprintf("ERROR EN TRAMO %d\n",i);

        fprintf("Movimiento: %.2f -> %.2f\n",q0,qf);
        fprintf("Velocidad máxima: %.2f\n",vmax);

        fprintf("\nTiempo solicitado: %.4f\n",Ttot);

        fprintf("El tiempo debe cumplir:\n");
        fprintf("%.4f < T < %.4f\n",Tmin,Tmax);

        return;
    end

    % Cantidad de muestras del tramo
    muestras = 300;

    % Generar trayectoria trapezoidal
    [q,qd,qdd] = trapveltraj( ...
        [q0 qf], ...
        muestras, ...
        "EndTime",Ttot, ...
        "PeakVelocity",vmax);

    % Tiempo local del tramo
    t_local = linspace(0,Ttot,muestras);

    % Convertir a tiempo global
    t_global = t_local + tiempo_global;

    % Evitar repetir muestras entre tramos
    if i > 1

        q        = q(:,2:end);
        qd       = qd(:,2:end);
        qdd      = qdd(:,2:end);

        t_global = t_global(2:end);
    end

    % Concatenar trayectoria
    Q   = [Q q];
    Qd  = [Qd qd];
    Qdd = [Qdd qdd];
    T   = [T t_global];

    % Actualizar tiempo acumulado
    tiempo_global = T(end);

end

%% Gráficas

figure;

subplot(3,1,1)
plot(T,Q,'LineWidth',2)
ylabel('Posición')
title('Trayectoria Trapezoidal Multitramo')
grid on

subplot(3,1,2)
plot(T,Qd,'LineWidth',2)
ylabel('Velocidad')
grid on

subplot(3,1,3)
plot(T,Qdd,'LineWidth',2)
ylabel('Aceleración')
xlabel('Tiempo')
grid on


%% Referencia para el sistema

t = T;
ref = [t; Qd]';