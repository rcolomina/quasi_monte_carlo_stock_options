# Test del estimador pathwise para Rho de una opcion call europea 
# INPUTS 
# S0    : precio subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo
# OUTPUT
# Rho   : d(precio)/d(sigma)

# Condiciones iniciales de la simulacion
S0=90;
K=100;
rate=0.1;
delta=0.03;
sigma=0.25;
T=0.2;

% Tamaño de la muestra aleatoria
N=10000;

% Generamos N muestras aleatorias de Z distribución normal estandar
Z=eye(N,1);
Z=stdnormal_rnd(N,1);

% Aplicamos las muestras al estimador pathwise de delta
% S0 = 90,100,110

ST=eye(N,1);
for i=1:N
    ST(i)=lognormal_random_ST(S0,rate,delta,sigma,T,Z(i));
endfor

RHO=eye(N,1);
for i=1:N
	 RHO(i)=european_call_estimador_pathwise_rho(S0,ST(i),K,rate,delta,sigma,T);
endfor
mean(RHO)
standard_error(RHO)

%S0=[90,100,110];
%for k=1:length(S0)
  % Calculamos ST lognormal variable aleatoria desde Z
%  ST=lognormal_random_ST(S0(k),rate,delta,sigma,T,Z);
%  for i=1:N
%	 VEGA(i)=european_call_estimator_pathwise_vega(S0(k),ST(i),K,rate,delta,sigma,T);
%  endfor
%  Vega=mean(VEGA)
% 
%endfor
