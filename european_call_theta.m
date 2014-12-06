#INPUTS 
# S0 : precio subyacente
# K :strike price, 
# rate : tipo interes
# delta : dividendo
# sigma : volatilidad
# T : periodo
#OUTPUT
# Theta -d(precio)/d(T)
function f_ret=european_call_theta(S0,K,rate,delta,sigma,T)
     d1= f_d1(S0,K,rate,delta,sigma,T);

     d2= d1 - sigma * sqrt(T); 

	  f_ret = - sigma * exp ( - delta * T ) * S0 * stdnormal_pdf(d1) / (2 * sqrt( T ) ) + delta * exp ( -delta * T ) * S0 * stdnormal_cdf(d1) - rate * K * exp( - rate * T ) * stdnormal_cdf(d2);
endfunction
