%% Procesamiento de Datos Reales y Modelado de Primer Orden
clear; clc; close all;

% 1. Parámetros del experimento
t_offset = 1.0; 
V_step = 8;     
load('Result1_Vel_real.mat'); 

% 2. Extraer y sincronizar datos
t_raw = vel_real(1,:); 
y_raw = vel_real(2,:);

t_re = t_raw - t_offset;
mask = t_re >= 0; 
t_re = t_re(mask);
y_re = y_raw(mask);

%% 3. Cálculos
v_final_re = mean(y_re(end-100:end)); 

% Tiempo de subida
idx10 = find(y_re >= 0.10 * v_final_re, 1);
idx90 = find(y_re >= 0.90 * v_final_re, 1);
tr_re = t_re(idx90) - t_re(idx10);

% Tiempo de asentamiento
idx_asent = find(abs(y_re - v_final_re) > 0.02 * v_final_re, 1, 'last');
ts_re = t_re(idx_asent + 1);

%% 4. Modelo de primer orden
K_real = v_final_re / V_step;
tau_real = ( (tr_re/2.2) + (ts_re/4) ) / 2;

% Punto 63.2%
v_tau = 0.632 * v_final_re;
idx_tau = find(y_re >= v_tau, 1);
t_tau = t_re(idx_tau);

s = tf('s');
G_identificada = K_real / (tau_real * s + 1);

%% 5. Mostrar resultados
fprintf('\n--- MODELO IDENTIFICADO (PRIMER ORDEN) ---\n');
fprintf('Ganancia (K): %.4f RPM/V\n', K_real);
fprintf('Constante de tiempo (tau): %.4f s\n', tau_real);
fprintf('------------------------------------------\n');

%% 6. Gráfica
figure('Color', 'w', 'Position', [100 100 1000 550]);

plot(t_re, y_re, 'Color', [0.6 0.6 0.6], ...
    'LineWidth', 2.5, 'DisplayName', 'Datos experimentales'); 
hold on;

[y_mod, t_mod] = step(V_step * G_identificada, max(t_re));
plot(t_mod, y_mod, 'r--', ...
    'LineWidth', 3, 'DisplayName', 'Modelo identificado');

% Línea estado estacionario
yline(v_final_re, 'b--', ...
    sprintf('V_{ss} = %.1f RPM', v_final_re), ...
    'LineWidth', 2, 'FontSize', 16);

% Línea 63.2%
yline(v_tau, 'g--', ...
    '63.2%', ...
    'LineWidth', 2, 'FontSize', 16);

% Línea vertical tau
xline(t_tau, 'k--', ...
    sprintf('\\tau = %.4f s', tau_real), ...
    'LineWidth', 2, 'FontSize', 16);

% Punto tau
plot(t_tau, v_tau, 'ko', ...
    'MarkerSize', 10, 'MarkerFaceColor', 'k');

% Texto del modelo
texto_modelo = sprintf('K = %.2f RPM/V\n\\tau = %.4f s', K_real, tau_real);
text(t_re(end)*0.6, v_final_re*0.4, texto_modelo, ...
    'FontSize', 18, ...
    'BackgroundColor', 'w', ...
    'EdgeColor', 'k');

% Configuración visual
grid on;
xlim([0, 1.5]);

title('Identificación de Modelo de Primer Orden', ...
    'FontSize', 20, 'FontWeight', 'bold');

xlabel('Tiempo (s)', ...
    'FontSize', 18, 'FontWeight', 'bold');

ylabel('Velocidad (RPM)', ...
    'FontSize', 18, 'FontWeight', 'bold');

set(gca, 'FontSize', 16, 'LineWidth', 1.5);

legend('Location', 'southeast', 'FontSize', 16);