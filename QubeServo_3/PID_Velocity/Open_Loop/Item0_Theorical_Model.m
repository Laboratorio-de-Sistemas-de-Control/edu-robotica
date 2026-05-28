%% Análisis Comparativo de Modelado y Muestreo - Qube-Servo 3
clear all; close all; clc;

%% 1. Parámetros Físicos Originales
R  = 7.5; L  = 1.15e-3; Kt = 0.0422; Kv = 0.0422;
bm = 0; Jeq = 18.3e-6; rad2rpm = 60 / (2*pi); 
s = tf('s');
V_test = 10;

%% 2. SECCIÓN 5: ANÁLISIS DE SEGUNDO ORDEN Y CRITERIO DE FRECUENCIA NATURAL
% Definición del modelo completo
G2_rads = Kt / ((Jeq*s + bm)*(L*s + R) + Kt*Kv);
G2_rpm = G2_rads * rad2rpm;

% Extracción de parámetros de 2do orden
[~, den2] = tfdata(G2_rads, 'v');
a = den2(1); b = den2(2); c = den2(3);
wn = sqrt(c/a); 
zeta = b / (2 * sqrt(a*c));
K2 = dcgain(G2_rpm);

% Muestreo basado en Frecuencia Natural (Criterio dinámico rápido)
wn_hz = wn / (2*pi);
fs_min_2seg = 20 * wn_hz;
Ts_max_2seg = 1 / fs_min_2seg;

fprintf('\n--- SECCIÓN 5: ANÁLISIS DE SEGUNDO ORDEN ---');
fprintf('\nModelo: G(s) = Kt / [(Jeq*s + bm)*(L*s + R) + Kt*Kv]');
fprintf('\nGanancia Estática (K):        %.2f RPM/V', K2);
fprintf('\nFrecuencia Natural (wn):      %.2f rad/s (%.2f Hz)', wn, wn_hz);
fprintf('\nFactor de Amortiguamiento (z): %.2f', zeta);
fprintf('\n--------------------------------------------------');
fprintf('\nCRITERIO DE MUESTREO (Basado en dinámica de 2do orden):');
fprintf('\nFrecuencia de Muestreo Mínima: %.2f Hz', fs_min_2seg);
fprintf('\nPeriodo de Muestreo Máximo:    %.4f s', Ts_max_2seg);
fprintf('\n--------------------------------------------------');
fprintf('\nARGUMENTO: Dado que z = %.2f (z >> 1), el sistema es altamente', zeta);
fprintf('\nsobreamortiguado. El polo eléctrico es despreciable frente al mecánico,');
fprintf('\npermitiendo una reducción a primer orden para diseño de control.\n');

% Plot Sección 5
figure('Name','Análisis Segundo Orden','Color','w');
step(V_test * G2_rpm, 0.5); grid on;
title('Respuesta al Escalón - Modelo de Segundo Orden');
ylabel('Velocidad (RPM)'); xlabel('Tiempo (s)');

%% 3. SECCIÓN 6: CARACTERIZACIÓN Y MUESTREO DE PRIMER ORDEN
% Simulación para obtener parámetros mediante inspección
[y, t] = step(V_test * G2_rpm, 2);
v_final = mean(y(end-10:end)); 
K1 = v_final / V_test;

% Cálculo de tiempos reales
t10 = t(find(y >= 0.10 * v_final, 1));
t90 = t(find(y >= 0.90 * v_final, 1));
tr = t90 - t10;
idx_asent = find(abs(y - v_final) > 0.02 * v_final, 1, 'last');
ts = t(idx_asent + 1);
tau_eq = ts / 4; % Basado en criterio del 2%

% Muestreo basado en respuesta temporal (Criterio de resolución)
% fs >= 10 / tr (para tener al menos 10 puntos en la subida)
fs_min_1er = 10 / tr;
Ts_max_1er = 1 / fs_min_1er;

fprintf('\n--- SECCIÓN 6: VALIDACIÓN Y PARÁMETROS DE PRIMER ORDEN ---');
fprintf('\nModelo Sugerido: G(s) = K / (tau*s + 1)');
fprintf('\nGanancia Estática (K):   %.2f RPM/V', K1);
fprintf('\nConstante de tiempo (t): %.4f s', tau_eq);
fprintf('\nRise Time (tr):          %.4f s', tr);
fprintf('\nSettling Time (ts):      %.4f s', ts);
fprintf('\n--------------------------------------------------');
fprintf('\nCRITERIO DE MUESTREO (Basado en respuesta temporal de 1er orden):');
fprintf('\nFrecuencia de Muestreo Mínima (10/tr): %.2f Hz', fs_min_1er);
fprintf('\nPeriodo de Muestreo Máximo (tr/10):    %.4f s', Ts_max_1er);
fprintf('\nFrecuencia QUARC recomendada:          500.00 Hz');
fprintf('\n--------------------------------------------------\n');

% Plot Sección 6
G1_tf = tf(K1, [tau_eq 1]);
figure('Name','Validación Primer Orden','Color','w');
plot(t, y, 'LineWidth', 2, 'DisplayName', 'Modelo Original (2do)'); hold on;
step(V_test * G1_tf, t(end), 'r--'); 
title('Comparativa: Modelo Original vs. Aproximación Primer Orden');
legend('Segundo Orden (Real)', 'Primer Orden (Aprox)');
ylabel('Velocidad (RPM)'); xlabel('Tiempo (s)'); grid on;