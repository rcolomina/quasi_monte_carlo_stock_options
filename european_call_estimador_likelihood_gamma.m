# Estimador likelihood ratio de Gamma para una opcion call europea
# INPUTS 
# S0    : precio subyacente en instante cero
# ST    : precio subyacente a final de periodo
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo 
# OUTPUT
# Delta d2(precio)/d2(S0)

function f_return=european_call_estimador_likelihood_gamma(S0,ST,K,rate,delta,sigma,T)

  aux1 = exp( - rate * T ) * max( ST - K, 0);

  aux2 = log( ST / S0 ) - ( rate - delta - 0.5 * sigma * sigma ) * T;
  d = aux2 / (sigma * sqrt(T));

  f_return = aux1 * ( d * d - d * sigma * sqrt(T) - 1 ) / ( S0 * S0 * sigma * sigma * T);

endfunction
