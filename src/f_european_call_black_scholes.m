# Black-Scholes para Opcion Call Europea
# INPUTS 
# S0    : precio inicial 
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo 
# OUTPUT
# precio de opcion call europea
function f_return=f_european_call_black_scholes(S0,K,rate,delta,sigma,T)
  d1 = ( log ( S0 / K ) + (rate - delta + 0.5 * sigma * sigma) * T ) / (sigma * sqrt(T));
  d2 = d1 - sigma * sqrt(T);
  f_return = S0 * exp ( - delta * T ) * stdnormal_cdf(d1) - exp ( - rate * T ) * K * stdnormal_cdf(d2);
endfunction
