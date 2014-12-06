#INPUTS 
# S0 : precio subyacente
# K :strike price, 
# rate : tipo interes
# delta : dividendo
# sigma : volatilidad
# T : periodo
#OUTPUT
# Delta d(precio)/dS0
function f_ret=european_call_delta(S0,K,rate,delta,sigma,T)
  f_ret = exp ( -delta * T ) * stdnormal_cdf( f_d1(S0,K,rate,delta,sigma,T) );
endfunction
