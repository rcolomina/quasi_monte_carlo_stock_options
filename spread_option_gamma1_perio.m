# SPREAD OPTIONS: CALCULO GAMMA primer subyacente
# INPUTS
# u1 en [0,1) :componente x del n-esimo termino de la serie de baja discrepancia
# u2 en [0,1) :componente y ...
# w1 y w2 : pesos de cada subyacente considerados positivos
# rate : tipo de interes
# delta1 y delta2 : dividendos para los subyacente 1 y 2
# S01 y S02 precios de los subyacente en el instante 0
# sigma1 y sigma2 son las volatilidades de los subyacentes
# ro12 en [-1,1] correlación entre los subyacentes
# T tiempo de madurez de las opciones
# K precio del strike del spread
# param : tipo de periodizacion aplicada
# OUTPUTS
# Valor de la griega delta1 para una Spread Option
#
function f_retorno = spread_option_gamma1_perio(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,param)
	  value=0;
     N=length(glp);
	  for i=1:N
				u1=f_periodifica(glp(i,1),param);
            u2=f_periodifica(glp(i,2),param);
			
            value_aux=hstar_gamma1(u1,u2,w1,w2,rate,delta1,delta2,S10,S20,sigma1,sigma2,ro12,T,K);
            value_aux=value_aux*f_periodifica_deriv(glp(i,1),param)*f_periodifica_deriv(glp(i,2),param);
            value=value+value_aux;
     endfor
     f_retorno=exp(-rate*T)*value/N;
endfunction
