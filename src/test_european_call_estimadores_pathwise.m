# Test Griegas Opcion Call Europe usando estimadores de tipo pathwise
#INPUTS 
# S0    : precio subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo
#OUTPUT
# Delta : d(precio)/d(S0)
# Vega  : d(precio)/d(sigma)
# Rho   : d(precio)/d(rate)
# Theta : -d(precio)/d(T)

% Condiciones iniciales 
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

S0=[90,100,110];
for k=1:length(S0)

  % Calculamos ST lognormal variable aleatoria desde Z
  ST=lognormal_random_ST(S0(k),rate,delta,sigma,T,Z);

  #DELTA
  DELTA=eye(N,1);
  for i=1:N
	 DELTA(i)=european_call_estimador_pathwise_delta(S0(k),ST(i),K,rate,T);
  endfor
  Delta=mean(DELTA)
  StandardErrorMeanDelta=standard_error(DELTA)

  #VEGA
  VEGA=eye(N,1);
  for i=1:N
	 VEGA(i)=european_call_estimador_pathwise_vega(S0(k),ST(i),K,rate,delta,sigma,T);
  endfor
  Vega=mean(VEGA)
  StandardErrorMeanVega=standard_error(VEGA)

  #RHO
  RHO=eye(N,1);
  for i=1:N
	 RHO(i)=european_call_estimador_pathwise_rho(S0(k),ST(i),K,rate,delta,sigma,T);
  endfor
  Rho=mean(RHO)
  StandardErrorMeanRho=standard_error(RHO)

  #THETA
  THETA=eye(N,1);
  for i=1:N
	 THETA(i)=european_call_estimador_pathwise_theta(S0(k),ST(i),K,rate,delta,sigma,T);
  endfor
  Theta=mean(THETA)
  StandardErrorMeanTheta=standard_error(THETA)

endfor





