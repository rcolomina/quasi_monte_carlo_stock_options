#INPUTS 
# S0 : precio subyacente
# K :strike price, 
# rate : tipo interes
# delta : dividendo
# sigma : volatilidad
# T : periodo
#OUTPUT
# Rho d(precio)/d(rate)
function f_ret=european_call_rho(S0,K,rate,delta,sigma,T)
     d1= f_d1(S0,K,rate,delta,sigma,T);
     d2= d1 - sigma * sqrt(T); 
	  f_ret = K * T * exp ( - rate * T ) * stdnormal_cdf(d2);
endfunction

