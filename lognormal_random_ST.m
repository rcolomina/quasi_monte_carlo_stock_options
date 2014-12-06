# INPUTS:
# S0 : precio inicial
# rate : tipo de interes
# delta : dividendo del subyacente
# sigma : volatilidad del subyacente
# T : periodo 
# Z : 

function f_ret=lognormal_random_ST(S0,rate,delta,sigma,T,Z)
  
  sigma2 = sigma * sigma;

  aux= exp ( ( rate - delta - sigma2 * 0.5) * T + sigma * sqrt( T ) * Z );

  f_ret= S0 * aux;

endfunction
