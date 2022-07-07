# Estimador pathwise para Rho de una opcion call europea
# INPUTS 
# S0    : precio inicial subyacente
# ST    : precio final subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo de maduracion
# OUTPUT
# Rho d(precio)/d(rate) (ST): Depende de la muestra
function f_return=european_call_estimador_pathwise_rho(S0,ST,K,rate,delta,sigma,T)

  if(ST>=K)
	 f_return = K * T * exp ( - rate * T );
  else
    f_return = 0;
  endif

endfunction
