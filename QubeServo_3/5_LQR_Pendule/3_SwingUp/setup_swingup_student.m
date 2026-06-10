clear; 
close all;
clc; 

%% Cargar parámetros
qube2_rotpen_param;

%% Calculo para swing up
%  Moment of inertia of pendulum about center of mass (kg-m^2)
Jp_cm = mp*Lp^2/12; % used to calculate pendulum energy in swing-up control

%% Cálculo para controlador
% Set open-loop state-space model of rotary single-inverted pendulum (SIP)
rotpen_ABCD_eqns_ip;
% Display matrices
A
B

%Q = eye(4);
Q = diag([1 50 1 1]);
R = 1;

% Ganancias del controlador
K = lqr(A,B,Q,R)