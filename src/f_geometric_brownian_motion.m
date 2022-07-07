# GEOMETRIC BROWNIAN MOTION

# INPUT : parametros del GBM
# T : periodo de generacion
# n : numero de pasos de la discretizacion
# rate : tipo de interes
# delta: dividentos
# sigma: volatilidad
# S0 : precio inicial

# Algoritmo de discretizacion : Aproximation de Euler
# S(i+1) = S(i) * ( 1 + (rate - delta) * DT + sigma * sqrt(DT) * Z)

# OUTPUT : vector con un GBM

function f_return = f_geometric_brownian_motion(T,n,rate,delta,sigma,S0)

  # Dt : diferencial de tiempo
  Delta_t=T/n;

  # reservamos memoria
  GEOBROWMOT=eye(n,1);

  # Algoritmo de discretizacion : Aproximation de Euler
  # S(i+1) = S(i) * ( 1 + (rate - delta) * DT + sigma * sqrt(DT) * Z)
  GEOBROWMOT(1)=S0;
#  GEOBROWMOT(1,2)=0;
  for i=2:n
    Z = normrnd(0,1);
    S0 = S0 * ( 1 + (rate - delta) * Delta_t + sigma * sqrt(Delta_t) * Z);
    GEOBROWMOT(i) = S0;
#    GEOBROWMOT(i,2) = i / n;
  endfor


  f_return=GEOBROWMOT;

endfunction



