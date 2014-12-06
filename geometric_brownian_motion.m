% GEOMETRIC BROWNIAN MOTION

% MODELO ecuacion diferencial
% dS_t= mu*S_t*dt+sigma*S_t*dB_t

% T  : perido de generacion
T=1;

% n  :numero de pasos de la discretizacion
n=500;

% Dt : diferencial de tiempo
Dt=T/n;

% rate : tipo de interes
rate=0.05;

% delta: dividentos
delta=0.05;

% sigma: desviacion tipicas
sigma=0.2;

% precio inicial
precio=10;

% reservamos memoria
GEOBROWMOT=eye(n,2);

% Algoritmo de discretizacion : Euler Aproximation
% S(i+1) = S(i) * ( 1 + (rate - delta) * DT + sigma * sqrt(DT) * Z)
GEOBROWMOT(1,1)=10;
GEOBROWMOT(1,2)=0;
for i=2:n
  Z = normrnd(0,1);
  precio = precio * ( 1 + (rate - delta) * Dt + sigma * sqrt(Dt) * Z);
  GEOBROWMOT(i,1) = precio;
  GEOBROWMOT(i,2) = i / n;
endfor




