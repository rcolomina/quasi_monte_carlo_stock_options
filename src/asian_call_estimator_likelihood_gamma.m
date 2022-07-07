# Estimador Likelihood de una opcion Call Asiática
# INPUTS 
# S0    : precio subyacente
# S     : vector de precios a cierre de dia
# K     : strike price 
# rate  : tipo de interés
# sigma : volatilidad
# T     : momento de maduración
# OUTPUT
# Gamma d2(precio)/d2(S0)
function f_return=asian_call_estimator_likelihood_gamma(S0,S,K,rate,delta,sigma,T)

  aux1 = exp(-rate*T)*max(mean(S)-K,0);

  m=length(S);
  Delta_t=1/365.25;%1.2060;
  d1=(log(S(2)/S(1))-(rate-delta-0.5*sigma*sigma)*Delta_t)/(sigma*sqrt(Delta_t));

  aux2=(d1*d1-d1*sigma*sqrt(Delta_t)-1)/(S0*S0*sigma*sigma*Delta_t);

  f_return=aux1*aux2;


endfunction
