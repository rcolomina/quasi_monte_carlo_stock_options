# INPUT
# asian : Estructura conteniendo los siguientes
## S0 : precio de arranque del subyacente
## K : strike price
## r : tipo de interes
## delta : dividendo del subyacente
## sigma : volatilidad
## m : numero de iteraciones
## T : Periodo de maduracion de la opcion
# set_points : Conjunto de puntos de integracion en [0,1)^m
# OUTPUT
# Valoracion de la opcion asiatica
#function f_return=asian_option_qmc(S0,K,r,delta,sigma,m,T,set_points)

function f_return=asian_option_qmc(asian_param,set_points)

   S0=asian_param.S0;
	K=asian_param.K;
	r=asian_param.r;
	delta=asian_param.delta;
	sigma=asian_param.sigma;
	m=asian_param.m;
	T=asian_param.T;

   N=length(set_points);
   v_valor=eye(N,1);
   for i=1:N

	  v_precio_promedio=eye(m,1);
	  
	  if(sum(set_points(i,:)>0)==length(set_points(i,:)))
		 Z=stdnormal_inv(set_points(i,:));
		 
	    for j=1:m
			v_precio_promedio(j)=f_gbm_explicit(S0,r,sigma,delta,j,T,Z);
		 endfor
	  else
        v_precio_promedio=0;
	  endif
     mean(v_precio_promedio);
     v_valor(i)=max(mean(v_precio_promedio)-K,0);

	endfor
   f_return=exp(-r*T)*mean(v_valor);
endfunction
