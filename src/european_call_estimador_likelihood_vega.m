# Estimador likelihood ratio de Vega para una opcion call europea
# INPUTS 
# S0    : precio subyacente en instante cero
# ST    : precio subyacente a final de periodo
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo 
# OUTPUT
# Delta d(precio)/d(sigma)

function f_return=european_call_estimador_likelihood_vega(S0,ST,K,rate,delta,sigma,T)

  aux1 = exp( - rate * T ) * max( ST - K, 0);

  aux2 = log( ST / S0 ) - ( rate - delta - 0.5 * sigma * sigma ) * T;
  d = aux2 / (sigma * sqrt(T));

  parcial_d_sigma = ( log( S0 / ST ) + ( rate - delta + 0.5 * sigma * sigma ) * T ) / (sigma * sigma * sqrt(T));

  f_return = aux1 * ( - d * parcial_d_sigma - 1 / sigma );

endfunction
