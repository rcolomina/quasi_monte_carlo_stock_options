# SPREAD OPTIONS
# INPUTS
# u1 en [0,1) :componente x del n-esimo termino de la serie de baja discrepancia
# u2 en [0,1) :componente y ...
# w1 y w2 : pesos de cada subyacente considerados positivos
# rate : tipo de interes
# delta1 y delta2 : dividendos para los subyacente 1 y 2
# S01 y S02 : precios de los subyacente en el instante 0
# sigma1 y sigma2 : volatilidades de los subyacentes
# ro12 en [-1,1] correlación entre los subyacentes
# T tiempo de madurez de las opciones en años
# K precio del ejercicio
# numsubyacente: subyacente para la que se quiere calcular la delta de la spread opción: valores posibles 1 o 2
# OUTPUTS
# Devuelve el valor de la griega delta i=1 o i=2 para una spread option
function f_retorno = spread_option_delta_perio(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,param,numsubyacente)
	  value=0;
     N=length(glp);
	  for i=1:N
				u1=f_periodifica(glp(i,1),param);
            u2=f_periodifica(glp(i,2),param);
			
            value_aux=hstar_delta2(u1,u2,w1,w2,rate,delta1,delta2,S10,S20,sigma1,sigma2,ro12,T,K,numsubyacente);
            value_aux=value_aux*f_periodifica_deriv(glp(i,1),param)*f_periodifica_deriv(glp(i,2),param);
            value=value+value_aux;
     endfor
     f_retorno=exp(-rate*T)*value/N;
endfunction
