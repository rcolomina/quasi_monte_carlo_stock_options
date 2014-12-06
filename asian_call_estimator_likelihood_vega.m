# Estimador Likelihood de una opcion Call Asiática
# INPUTS 
# S0    : precio subyacente
# S     : vector de precios a cierre de dia
# K     : strike price 
# rate  : tipo de interés
# delta : dividendo
# sigma : volatilidad
# T     : momento de maduración
# OUTPUT
# Vega d(precio)/d(sigma)
function f_return=asian_call_estimator_likelihood_vega(S0,S,K,rate,delta,sigma,T)

  m=length(S);

  aux1 = exp(-rate*T)*max(mean(S)-K,0);

  Delta_t=1.2060;
  
  d1=(log(S(1)/S(1))-(rate-delta-0.5*sigma*sigma)*Delta_t)/(sigma*sqrt(Delta_t));
  parcial_d1_sigma=(log(S(1)/S(1))+(rate-delta+0.5*sigma*sigma)*Delta_t)/(sigma*sigma*sqrt(Delta_t));

  v_aux=-d1*parcial_d1_sigma-1/sigma;


  Delta_t = 1/365.25;%(T-(m-i)/365.25)-(T-(m-i+1)/365.25); 
  for i=2:m

	 di=(log(S(i)/S(i-1))-(rate-delta-0.5*sigma*sigma)*Delta_t)/(sigma*sqrt(Delta_t));
	 parcial_di_sigma=(log(S(i-1)/S(i))+(rate-delta+0.5*sigma*sigma)*Delta_t)/(sigma*sigma*sqrt(Delta_t));

	 v_aux(i)=-di*parcial_di_sigma-1/sigma;
  endfor

  aux2=sum(v_aux);

  f_return=aux1*aux2;


endfunction
