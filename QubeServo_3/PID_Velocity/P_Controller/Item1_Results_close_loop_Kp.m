% =========================================================================
% Análisis de Respuesta en Lazo Cerrado (Control Proporcional)
% Motor: Qube Servo 3
% =========================================================================
clear; clc; close all;

% 1. Cargar los datos del lazo cerrado
nombre_archivo = 'Res0_close_loop_Kp.mat';
load(nombre_archivo); 

% Extraer tiempo y velocidad
tiempo = vel(1, :);
velocidad = vel(2, :);

% 2. Calcular estado estacionario (antes de detectar inicio)
idx_estacionario = find(tiempo > (tiempo(end) - 1)); 
v_ss = mean(velocidad(idx_estacionario));

% 3. Detectar inicio del escalón (método mejorado: 2% del valor final)
umbral = 0.01 * v_ss;
idx_inicio = find(velocidad > umbral, 1);

if isempty(idx_inicio)
    error('No se detectó el inicio del sistema.');
end

t_inicio = tiempo(idx_inicio);

% 4. Calcular constante de tiempo (63.2%)
v_63 = v_ss * 0.632;

idx_tau = find(velocidad >= v_63, 1);

% Interpolación para mayor precisión
t_tau_absoluto = interp1(velocidad(idx_tau-1:idx_tau+1), ...
                         tiempo(idx_tau-1:idx_tau+1), v_63);

tau_lc = t_tau_absoluto - t_inicio;

% 5. Mostrar resultados
disp('======================================================');
disp('    RESULTADOS EXPERIMENTALES L. CERRADO (Control P)  ');
disp('======================================================');
fprintf('Referencia aplicada:       1789.40 RPM\n');
fprintf('Velocidad estacionaria:    %.2f RPM\n', v_ss);
fprintf('Constante de tiempo (tau): %.4f s\n', tau_lc);
disp('======================================================');

% 6. Gráfica
figure('Name', 'Lazo Cerrado - Qube Servo 3', ...
       'Color', 'w', ...
       'Position', [100 100 1000 550]);

plot(tiempo, velocidad, 'b-', 'LineWidth', 2.5); hold on;

% Línea de referencia
yline(1789.4, 'g--', 'Referencia (1789.4 RPM)', ...
    'LineWidth', 2, 'FontSize', 16);

% Estado estacionario
yline(v_ss, 'r--', sprintf('V_{ss} = %.1f RPM', v_ss), ...
    'LineWidth', 2, 'FontSize', 16);

% Inicio corregido
xline(t_inicio, 'k:', 'Inicio', ...
    'LineWidth', 2, 'FontSize', 16);

% Línea 63.2%
yline(v_63, 'g--', '63.2%', ...
    'LineWidth', 2, 'FontSize', 16);

% Punto tau
plot(t_tau_absoluto, v_63, 'ro', ...
    'MarkerSize', 10, 'MarkerFaceColor', 'r');

% Línea vertical tau
xline(t_tau_absoluto, 'r--', ...
    sprintf('\\tau = %.4f s', tau_lc), ...
    'LineWidth', 2, 'FontSize', 16);

% Configuración visual
grid on;

xlabel('Tiempo (s)', 'FontSize', 18, 'FontWeight', 'bold');
ylabel('Velocidad (RPM)', 'FontSize', 18, 'FontWeight', 'bold');

title('Respuesta al Escalón en Lazo Cerrado (Control P)', ...
      'FontSize', 20, 'FontWeight', 'bold');

set(gca, 'FontSize', 16, 'LineWidth', 1.5);

legend('Velocidad medida', 'Referencia', 'Estado estacionario', ...
       'Inicio', '63.2%', 'Punto \tau', ...
       'Location', 'southeast', ...
       'FontSize', 16);

% Ajuste de ejes
xlim([t_inicio - 0.05, t_inicio + 0.3]);
ylim([0, 2100]);