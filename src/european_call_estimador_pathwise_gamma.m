# Estimador pathwise de Gamma para una opcion call europea: FORMULA EXACTA
# INPUTS 
# S0    : precio subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo 
# OUTPUT
# Gamma d2(precio)/d2(S0) 
function f_return=european_call_estimador_pathwise_gamma(S0,K,rate,delta,sigma,T)

  nd1 = stdnormal_pdf( f_d1(S0,K,rate,delta,sigma,T) );

  aux = S0 * sigma * sqrt(T);

  f_return = exp ( - delta * T ) * nd1 / aux; 

endfunction
