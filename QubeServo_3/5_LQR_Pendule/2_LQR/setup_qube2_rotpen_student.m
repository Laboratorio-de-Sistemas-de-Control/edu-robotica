%% Load Model
qube2_rotpen_param;
% Set open-loop state-space model of rotary single-inverted pendulum (SIP)
rotpen_ABCD_eqns_ip;
% Display matrices
A
B

%Q = eye(4);
Q = diag([10 1 1 1]);
R = 1;

K = lqr(A,B,Q,R)