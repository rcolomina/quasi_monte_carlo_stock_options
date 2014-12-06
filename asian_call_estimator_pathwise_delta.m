# Estimador pathwise de una opcion Call Asiática
# INPUTS 
# S0    : precio subyacente
# S     : vector de precios a cierre de dia
# K     : strike price 
# rate  : tipo de interés
# T     : momento de maduración
# OUTPUT
# Delta d(precio)/dS0
function f_return=asian_call_estimator_pathwise_delta(S0,S,K,rate,T)

  mediaPrecios=mean(S);

  if( mediaPrecios >= K )
    f_return = exp( - rate * T ) * mediaPrecios / S0;
  else
	 f_return = 0;
  endif


endfunction
