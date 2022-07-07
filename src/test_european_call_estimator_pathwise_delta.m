# Test del estimador de una opcion call europea usando pathwise
#INPUTS 
# S0    : precio subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo
#OUTPUT
# Delta d(precio)/dS0

% Condiciones iniciales de la simulacion
S0=90;
K=100;
rate=0.1;
delta=0.03;
sigma=0.25;
T=0.2;
% Tamaño de la muestra aleatoria
N=10000;
% Generamos N muestras aleatorias de Z distribución normal estandar
Z=stdnormal_rnd(N,1);
% Aplicamos las muestras al estimador pathwise de delta
% S0 = 90,100,110
S0=[90,100,110];
for k=1:length(S0)
  % Calculamos ST lognormal variable aleatoria desde Z
  ST=lognormal_random_ST(S0(k),rate,delta,sigma,T,Z);
  for i=1:N
	 DELTA(i)=european_call_estimator_pathwise_delta(S0(k),ST(i),K,rate,T);
  endfor
  Delta=mean(DELTA)
  StandardErrorMeanDelta=standard_error(DELTA)
endfor





