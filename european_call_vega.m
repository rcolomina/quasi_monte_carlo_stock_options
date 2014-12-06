#INPUTS 
# S0 : precio subyacente
# K :strike price, 
# rate : tipo interes
# delta : dividendo
# sigma : volatilidad
# T : periodo
#OUTPUT
# Delta d(precio)/d(sigma)
function f_ret=european_call_vega(S0,K,rate,delta,sigma,T)
	  f_ret = sqrt(T) * S0 * exp ( -delta * T ) * stdnormal_pdf( f_d1(S0,K,rate,delta,sigma,T) );
endfunction
