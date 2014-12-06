# Estimador pathwise de una opcion Call Asiática
# INPUTS 
# S0    : precio subyacente
# S     : vector de precios a cierre de dia
# K     : strike price 
# rate  : tipo de interés
# delta : dividendo
# sigma : volatilidad
# T     : momento de maduración
# OUTPUT
# Vega d(precio)/d(sigma)
function f_return=asian_call_estimator_pathwise_vega(S0,S,K,rate,delta,sigma,T)

  mediaP=mean(S);
  if( mediaP >= K )
    aux1 = exp( - rate * T );
  
	 m=length(S);
	 for i=1:m
		aux21=S(i);
		t = T - ( m - i ) / 365.25;
		aux22 = log ( S(i) / S0 ) + (rate - delta + 0.5 * sigma * sigma ) * t;
		v_aux(i)=aux21*aux22;
	 endfor
	 aux2 = (1/sigma) * mean(v_aux);

	 f_return = aux1 * aux2;
  else
	 f_return = 0;
  endif




endfunction
