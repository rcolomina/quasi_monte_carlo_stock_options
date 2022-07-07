# Función auxiliar
# INPUT : S0,x,rate,delta,sigma,T
# OUTPUT: d1(x) valor auxiliar
function f_ret=f_d1(S0,x,rate,delta,sigma,T)
	  f_ret= ( log ( S0 / x ) + ( rate - delta + 0.5 * sigma * sigma ) * T ) / ( sigma * sqrt( T ));
endfunction
