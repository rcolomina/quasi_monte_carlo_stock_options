# FORMULAD DE MARGRABE: PRECIO DE UNA SPREAD OPTION CON K=0 
# INPUTS
# S01,S02 : precios de los subyacente en el instante 0  (numero decimal positivo)
# delta1,delta2 : dividendo subyacente 1 y 2   (numero decimal positivo)
# sigma1,sigma2 : volatilidades de los subyacentes  (numero decimal positivo)
# ro12 : Correlacion entre subyacente en [-1,1] 
# T tiempo de madurez de las opciones (expresar en anhos)
# OUTPUT
# Valoracion de una spread option con k=0

function f_ret=margrabe_formula(S10,S20,delta1,delta2,sigma1,sigma2,ro12,T)

	  sigma=sqrt(sigma1*sigma1+sigma2*sigma2-2*sigma1*sigma2*ro12);
     d2=(log(S20/S10)+(delta1-delta2+sigma*sigma/2)*T)/(sigma*sqrt(T));
     d1=d2-sigma*sqrt(T);
     f_ret=exp(-delta2*T)*S20*stdnormal_cdf(d2)-exp(-delta1*T)*S10*stdnormal_cdf(d1);

endfunction
