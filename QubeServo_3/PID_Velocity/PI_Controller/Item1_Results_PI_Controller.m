% Analizador de Resultados del Controlador PI (Motor Quanser)
clear; clc; close all;

%% 1. Cargar archivo
filename = 'Res0_close_loop_PI.mat';
if ~isfile(filename)
    error('No se encontró el archivo. Verifica la ruta.');
end
data = load(filename);

%% 2. Extraer datos
varNames = fieldnames(data);
mainVar = data.(varNames{1});

if isa(mainVar, 'timeseries')
    t = mainVar.Time;
    y = mainVar.Data;
elseif ismatrix(mainVar) && size(mainVar,1)==2
    t = mainVar(1,:)';
    y = mainVar(2,:)';
else
    try
        t = mainVar.time;
        y = mainVar.signals.values;
    catch
        error('Formato de datos no reconocido.');
    end
end

% Asegurar formato columna
t = double(t(:));
y = double(y(:));

%% 3. Cálculos
n = length(y);

% Estado estacionario (promedio último 10%)
idx_ss = round(0.9*n):n;
y_ss = mean(y(idx_ss));

% Overshoot
y_max = max(y);
if y_max > 1.01*y_ss
    overshoot = ((y_max - y_ss)/y_ss)*100;
else
    overshoot = 0;
end

% Tiempo característico (63.2%)
target_tau = 0.632*y_ss;
idx_tau = find(y >= target_tau,1,'first');

if ~isempty(idx_tau)
    tau = t(idx_tau) - t(1);
else
    tau = NaN;
end

%% 4. Consola
fprintf('\n=============================================\n');
fprintf('   ANÁLISIS DEL CONTROLADOR PI\n');
fprintf('=============================================\n');
fprintf('Velocidad en estado estable : %.2f RPM\n', y_ss);
fprintf('Sobreimpulso               : %.2f %%\n', overshoot);
fprintf('Tiempo característico (63%%): %.4f s\n', tau);
fprintf('=============================================\n\n');

%% 5. Gráfica
figure('Color','w','Name','Respuesta del Motor','Position',[100 100 900 500]);

plot(t,y,'b','LineWidth',2.5); hold on;

% Línea estado estable SIN label automático
yline(y_ss,'r--','LineWidth',2.5);

% Posición horizontal (un poco a la derecha)
x_pos = t(round(0.2*length(t))); % 75% del eje x

% Texto manual
text(x_pos, y_ss, sprintf('SS = %.1f RPM',y_ss),...
    'FontSize',16,...
    'Color','r',...
    'VerticalAlignment','bottom',...
    'HorizontalAlignment','left');

% Punto máximo
if overshoot > 0
    plot(t(y==y_max),y_max,'ro','MarkerFaceColor','r','MarkerSize',10);
end

% Punto tau
if ~isnan(tau)
    plot(t(idx_tau),y(idx_tau),'go','MarkerFaceColor','g','MarkerSize',10);
    
    % línea vertical tau
    xline(t(idx_tau),'g--',...
        sprintf('\\tau = %.3f s',tau),...
        'LineWidth',2.5,...
        'FontSize',16,...
        'LabelVerticalAlignment','bottom');
end

ylim([0 3000]);
xlim([0 5]);

% Etiquetas GRANDES
title('Respuesta de Velocidad del Motor DC',...
    'FontSize',20,'FontWeight','bold');

xlabel('Tiempo (s)','FontSize',18);
ylabel('Velocidad (RPM)','FontSize',18);

% Números de ejes grandes
set(gca,'FontSize',16,'LineWidth',1.5);

grid on;

% Leyenda grande
if overshoot > 0
    legend('Respuesta','Estado Estable','Pico Máximo','63.2%',...
        'Location','southeast','FontSize',16);
else
    legend('Respuesta','Estado Estable','63.2%',...
        'Location','southeast','FontSize',16);
end