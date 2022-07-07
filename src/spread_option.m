# INPUT
# set_points : Conjuto de puntos del dominio de integración [0,1)^s
# w1, w2 : pesos de la spread
# rate : tipo de interes
# K precio de ejercicio
# S10, S20: precios iniciales de los subyacentes
# delta1, delta2 : dividendo de los subyacentes
# sigma1, sigma2 : volatilidades de los subyacentes
# ro12 : coeficiente de correlacion entre los subyacentes
# T : periodo de maduracion
# OUTPUT
# Valor de la Spread Option
function f_retorno = spread_option(set_points,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T)
	  value=0;
     N=length(set_points);
	  for i=1:N
			value=value+hstar(set_points(i,1),set_points(i,2),w1,w2,rate,delta1,delta2,S10,S20,sigma1,sigma2,ro12,T,K);
     endfor
     f_retorno=exp(-rate*T)*value/N;
endfunction
