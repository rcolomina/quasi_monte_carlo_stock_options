# Estimador pathwise para Theta de una Opcion call Europea
# INPUTS 
# S0    : precio inicial subyacente
# ST    : precio final subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo de maduracion
# OUTPUT
# Theta (-d(precio)/d(T)) (ST): Depende de la muestra
function f_return=european_call_estimador_pathwise_theta(S0,ST,K,rate,delta,sigma,T)

  if(ST>=K)
	 unoSTK=1;
  else
	 unoSTK=0;
  endif

  sigma2 = sigma * sigma;

  aux1 = rate * exp ( - rate * T ) * max( ST - K, 0 ); 

  aux2 = exp ( -rate * T ) * ST / ( 2 * T ) * ( log(ST/S0) + (rate - delta - 0.5 * sigma2) * T );

  f_return = aux1 - unoSTK * aux2;


endfunction
