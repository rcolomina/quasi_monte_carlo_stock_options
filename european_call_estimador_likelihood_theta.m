# Estimador likelihood ratio de Theta para una opcion call europea
# INPUTS 
# S0    : precio subyacente en instante cero
# ST    : precio subyacente a final de periodo
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo 
# OUTPUT
# Delta -d(precio)/d(T)

function f_return=european_call_estimador_likelihood_theta(S0,ST,K,rate,delta,sigma,T)

  aux1 = exp( - rate * T ) * max( ST - K, 0);

  aux2 = log( ST / S0 ) - ( rate - delta - 0.5 * sigma * sigma ) * T;
  d = aux2 / (sigma * sqrt(T));

  parcial_d_T = ( -log( ST / S0 ) - ( rate - delta - 0.5 * sigma * sigma ) * T ) / ( 2 * sigma * power(T,3/2));

  f_return = aux1 * ( rate + d * parcial_d_T + 1/ (2*T) );

endfunction
