#INPUTS 
# S0 : precio subyacente
# K :strike price, 
# rate : tipo interes
# delta : dividendo
# sigma : volatilidad
# T : periodo
#OUTPUT
# Gamma d2(precio)/d2(S0)
function f_ret=european_call_gamma(S0,K,rate,delta,sigma,T)
     d1=f_d1(S0,K,rate,delta,sigma,T);
	  f_ret = exp ( - delta * T ) * stdnormal_pdf(d1) / ( sigma * S0 * sqrt(T));
endfunction
