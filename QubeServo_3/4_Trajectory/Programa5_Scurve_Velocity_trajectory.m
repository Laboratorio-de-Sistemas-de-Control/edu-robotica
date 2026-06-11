%% Trayectoria en S de 7 Fases — Perfil Cinemático Articular
%
% Genera el perfil de posición, velocidad, aceleración y jerk para una
% trayectoria en S con jerk limitado. Evalúa las fronteras matemáticas
% para garantizar que el movimiento sea físicamente posible.

%% ── 1. DATOS DE USUARIO ──────────────────────────────────────────────
q_o     = 0.0;   % [rad]    Posición articular inicial
q_f     = 100.0; % [rad]    Posición articular final
qdot_s  = 15.0;   % [rad/s]  Velocidad de consigna (máxima)
qddot_s = 5.0;   % [rad/s²] Aceleración máxima permitida
j_m     = 5.0;   % [rad/s³] Jerk máximo permitido

%% ── 2. CÁLCULO DE PARÁMETROS Y VALIDACIÓN INTELIGENTE ────────────────
% Asumimos que la posición inicial (q_o), final (q_f) y la velocidad (qdot_s) 
% son fijas y deseadas por el usuario.
dist_total = abs(q_f - q_o);

% Frontera 1: Aceleración mínima absoluta (asumiendo jerk infinito)
a_min_abs = (qdot_s^2) / dist_total;

% Calculamos los parámetros temporales teóricos con los datos del usuario
dv1 = qddot_s^2 / (2 * j_m);
dv2 = qdot_s - 2 * dv1;
dist_min_req = (qdot_s * qddot_s / j_m) + (qdot_s^2 / qddot_s); % 2 * S_acel

% ── EVALUACIÓN DE FRONTERAS FÍSICAS ──
% Si dv2 < 0 (falla perfil triangular) o la distancia no alcanza...
if dv2 < 0 || dist_total < dist_min_req
    fprintf('\n[!] ERROR DE PARÁMETROS: La trayectoria no es realizable.\n');
    fprintf('Mantenemos fijos: Distancia = %.4f rad, Velocidad = %.4f rad/s\n\n', dist_total, qdot_s);
    
    fprintf('--> 1. RANGO PARA LA ACELERACIÓN MÁXIMA (qddot_s):\n');
    fprintf('    Debe ser ESTRICTAMENTE MAYOR a : %.4f [rad/s²]\n', a_min_abs);
    
    if qddot_s <= a_min_abs
        fprintf('    (Tu aceleración actual %.4f es demasiado baja. Ni con jerk infinito alcanza).\n\n', qddot_s);
    else
        fprintf('    (Tu aceleración actual %.4f es VÁLIDA. El problema está en el Jerk).\n\n', qddot_s);
    end
    
    fprintf('--> 2. RANGO PARA EL JERK MÁXIMO (j_m) (dada tu aceleración de %.4f):\n', qddot_s);
    if qddot_s > a_min_abs
        % Evaluamos si la restricción dominante es la distancia o la velocidad
        if qddot_s <= (2 * a_min_abs)
            j_min = (qdot_s * qddot_s^2) / (qddot_s * dist_total - qdot_s^2);
        else
            j_min = qddot_s^2 / qdot_s;
        end
        fprintf('    Debe ser MAYOR O IGUAL a       : %.4f [rad/s³]\n', j_min);
        fprintf('    (Tu jerk actual es %.4f).\n\n', j_m);
    else
        fprintf('    Primero debes aumentar la aceleración por encima de %.4f \n', a_min_abs);
        fprintf('    para poder calcular un valor de Jerk válido.\n\n');
    end
    
    error('Ejecución detenida: Ajusta qddot_s y j_m según los rangos matemáticos sugeridos.');
end

% Si pasa las validaciones, calculamos los tiempos base
tau1 = qddot_s / j_m;
tau2 = dv2 / qddot_s;
tau_cte = (dist_total - dist_min_req) / qdot_s;

% Velocidades intermedias
qdot1 = dv1;
qdot2 = qdot_s - dv1;

%% ── 3. POSICIONES AL INICIO DE CADA FASE ────────────────────────────
q1 = q_o   + (j_m/6)*tau1^3;
q2 = q1    + qdot1*tau2 + (qddot_s/2)*tau2^2;
q3 = q2    + qdot2*tau1 + (qddot_s/2)*tau1^2 - (j_m/6)*tau1^3;
q4 = q3    + qdot_s*tau_cte;
q5 = q4    + qdot_s*tau1 - (j_m/6)*tau1^3;
q6 = q5    + qdot2*tau2  - (qddot_s/2)*tau2^2;

%% ── 4. INSTANTES DE TRANSICIÓN ───────────────────────────────────────
t_tr = cumsum([0, tau1, tau2, tau1, tau_cte, tau1, tau2, tau1]);
T_total = t_tr(end);

%% ── 5. EVALUACIÓN DEL PERFIL CINEMÁTICO ─────────────────────────────
N  = 3000;                        
t  = linspace(0, T_total, N);     
q     = zeros(1,N);
qdot  = zeros(1,N);
qddot = zeros(1,N);
jerk  = zeros(1,N);

for k = 1:N
    tk = t(k);
    if tk <= t_tr(2)
        tp = tk - t_tr(1);
        jerk(k) = j_m; qddot(k) = j_m*tp; qdot(k) = (j_m/2)*tp^2; q(k) = q_o + (j_m/6)*tp^3;
    elseif tk <= t_tr(3)
        tp = tk - t_tr(2);
        jerk(k) = 0; qddot(k) = qddot_s; qdot(k) = qdot1 + qddot_s*tp; q(k) = q1 + qdot1*tp + (qddot_s/2)*tp^2;
    elseif tk <= t_tr(4)
        tp = tk - t_tr(3);
        jerk(k) = -j_m; qddot(k) = qddot_s - j_m*tp; qdot(k) = qdot2 + qddot_s*tp - (j_m/2)*tp^2; q(k) = q2 + qdot2*tp + (qddot_s/2)*tp^2 - (j_m/6)*tp^3;
    elseif tk <= t_tr(5)
        tp = tk - t_tr(4);
        jerk(k) = 0; qddot(k) = 0; qdot(k) = qdot_s; q(k) = q3 + qdot_s*tp;
    elseif tk <= t_tr(6)
        tp = tk - t_tr(5);
        jerk(k) = -j_m; qddot(k) = -j_m*tp; qdot(k) = qdot_s - (j_m/2)*tp^2; q(k) = q4 + qdot_s*tp - (j_m/6)*tp^3;
    elseif tk <= t_tr(7)
        tp = tk - t_tr(6);
        jerk(k) = 0; qddot(k) = -qddot_s; qdot(k) = qdot2 - qddot_s*tp; q(k) = q5 + qdot2*tp - (qddot_s/2)*tp^2;
    else
        tp = tk - t_tr(7);
        jerk(k) = j_m; qddot(k) = -qddot_s + j_m*tp; qdot(k) = qdot1 - qddot_s*tp + (j_m/2)*tp^2; q(k) = q6 + qdot1*tp - (qddot_s/2)*tp^2 + (j_m/6)*tp^3;
    end
end

%% ── 6. RESUMEN EN CONSOLA ────────────────────────────────────────────
fprintf('\n══════════════ Trayectoria en S — Parámetros ══════════════\n');
fprintf('  tau1    = %.4f s   (duración fase curva)\n',       tau1);
fprintf('  tau2    = %.4f s   (duración fase lineal)\n',      tau2);
fprintf('  tau_cte = %.4f s   (duración velocidad constante)\n',  tau_cte);
fprintf('  T_total = %.4f s\n',                               T_total);
fprintf('  qdot1   = %.4f rad/s  (vel. al final de F1)\n',    qdot1);
fprintf('  qdot2   = %.4f rad/s  (vel. al final de F2)\n',    qdot2);
fprintf('  S_acel  = %.4f rad    (distancia de aceleración)\n', dist_min_req/2);
fprintf('  q(T)    = %.4f rad    (debe ser q_f = %.4f)\n', q(end), q_f);
fprintf('═══════════════════════════════════════════════════════════\n\n');

%% ── 7. GRAFICACIÓN ───────────────────────────────────────────────────
nombres_fase  = {'F1','F2','F3','F4','F5','F6','F7'};
color_pos     = [0.08  0.40  0.74];
color_vel     = [0.00  0.60  0.85];
color_acel    = [0.80  0.15  0.15];
color_jerk    = [0.45  0.45  0.45];
color_sep     = [0.75  0.75  0.75];

fig = figure('Name','Trayectoria en S — 7 Fases', ...
             'NumberTitle','off','Color','w','Position',[80 50 860 720]);

ax1 = subplot(4,1,1);
plot(t, q, 'Color', color_pos, 'LineWidth', 2); hold on;
yline(q_o,'--','Color',color_sep,'LineWidth',0.8);
yline(q_f,'--','Color',color_sep,'LineWidth',0.8);
ylabel('q(t)  [rad]','FontSize',10);
title('Posición articular','FontWeight','bold','FontSize',10);
ylim([q_o - 0.1*(q_f-q_o), q_f + 0.15*(q_f-q_o)]); grid on; box off;

ax2 = subplot(4,1,2);
plot(t, qdot, 'Color', color_vel, 'LineWidth', 2); hold on;
yline(qdot_s,'--','Color',color_sep,'LineWidth',0.8);
ylabel('{\itq}{\bullet}(t)  [rad/s]','FontSize',10);
title('Velocidad articular','FontWeight','bold','FontSize',10);
ylim([-0.05*qdot_s, 1.25*qdot_s]); grid on; box off;

ax3 = subplot(4,1,3);
plot(t, qddot, 'Color', color_acel, 'LineWidth', 2); hold on;
yline(0,'Color',color_sep,'LineWidth',0.8);
ylabel('{\itq}{\bullet\bullet}(t)  [rad/s²]','FontSize',10);
title('Aceleración articular','FontWeight','bold','FontSize',10);
ylim(1.4*[-qddot_s, qddot_s]); grid on; box off;

ax4 = subplot(4,1,4);
plot(t, jerk, 'Color', color_jerk, 'LineWidth', 2); hold on;
yline(0,'Color',color_sep,'LineWidth',0.8);
ylabel('{\itq}{\bullet\bullet\bullet}(t)  [rad/s³]','FontSize',10);
title('Jerk (tirón)','FontWeight','bold','FontSize',10);
xlabel('Tiempo [s]','FontSize',10);
ylim(1.5*[-j_m, j_m]); grid on; box off;

for ax = [ax1, ax2, ax3, ax4]
    axes(ax); %#ok<LAXES>
    for i = 2:8
        xline(t_tr(i), '--', 'Color', color_sep, 'LineWidth', 0.8);
    end
    if ax == ax2
        ylims = ylim; y_lbl = ylims(2) * 0.90;
        for i = 1:7
            t_mid = (t_tr(i) + t_tr(i+1)) / 2;
            text(t_mid, y_lbl, nombres_fase{i}, 'HorizontalAlignment','center', 'FontSize',7,'Color',[0.5 0.5 0.5]);
        end
    end
end
linkaxes([ax1 ax2 ax3 ax4], 'x');
xlim([0, T_total]);



% Crear referencia para el controlador
ref = [t; qdot]';