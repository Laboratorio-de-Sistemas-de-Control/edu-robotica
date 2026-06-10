%% PROGRAMA DE DEMSTRACIÓN EN CLASE

%% Definimos los parámetros de posición objetivo
q0 = 0;      % rad
qf = 100;     % rad
T_total = 5; % segundos

t = linspace(0, T_total, 1000);

%% Condición:
% Se puede añadir la restricción de velocidad máxima del motor del QUbe
% servo 3, incide en el tiempo. 


%% Calculamos: posición, velocidad y aceleración
a1 = (qf-q0)/T_total;  % Velocidad 
a0 = q0-a1*0;          % escalar para graficar la posición

% Definimos el vector de posición en el tramo
vec_q = a1.*t+a0; 

% Definimos el vector de velocidad en todo el tramo
vec_qd  = ones(size(t))*a1;  % rad/s

% Definimos el vector de aceleración en el tramo 
vec_qdd = zeros(size(t));    

% Mapear al vector de referencia del controlador
ref = [t;  vec_qd]';

%% Gráfica de los resultados

subplot(3, 1, 1);
plot(t, vec_q, "LineWidth",2);
hold on; 
plot(0, q0, "ro", "MarkerSize",8, "MarkerFaceColor","r");
hold on; 
plot(T_total, qf, "ro", "MarkerSize",8, "MarkerFaceColor","r");
legend("Posición");
grid on; 

subplot(3, 1, 2); 
plot(t, vec_qd, "LineWidth",2); 
hold on; 
legend("Velocidad"); 
grid on; 

subplot(3, 1, 3); 
plot(t, vec_qdd, "LineWidth",2); 
hold on; 
legend("Aceleración"); 
grid on; 

