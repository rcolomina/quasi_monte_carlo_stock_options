# INPUT
# glp : Conjuto de puntos del dominio de integración [0,1)^s
# w1, w2 : pesos de la spread
# rate : tipo de interes
# K precio de ejercicio
# S10, S20: precios iniciales de los subyacentes
# delta1, delta2 : dividendo de los subyacentes
# sigma1, sigma2 : volatilidades de los subyacentes
# ro12 : coeficiente de correlacion entre los subyacentes
# T : periodo de maduracion
# param : parametro de periodizacion comprendido en [1,2,3,4,5,6,7,8]
# OUTPUT
# Valor de la Spread Option
function f_retorno = spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,param)
	  value=0;
     N=length(glp);
	  for i=1:N	 
				u1=f_periodifica(glp(i,1),param);
            u2=f_periodifica(glp(i,2),param);
            value_aux=hstar(u1,u2,w1,w2,rate,delta1,delta2,S10,S20,sigma1,sigma2,ro12,T,K);
            value_aux=value_aux*f_periodifica_deriv(glp(i,1),param)*f_periodifica_deriv(glp(i,2),param);
            value=value+value_aux;
     endfor
     f_retorno=exp(-rate*T)*value/N;
endfunction
