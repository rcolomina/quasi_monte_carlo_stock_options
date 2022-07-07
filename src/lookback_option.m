##############################################
# Autor   : Ruben Colomina Citoler
# Fecha   : 30-08-2013
##############################################
# INPUTS
# S0 : precio de arranque del subyacente
# K  : precio del strike 
# r  : tipo de interes
# delta : dividendo del subyacente
# sigma : volatilidad
# T  : periodo de maduracion de la opcion
# set_points : conjunto de puntos de Nxm  en [0,1)^m
# siendo N numero de puntos y m la dimension
#        
##############################################
# OUTPUT
# Valoracion de una opcion lookback discreta
##############################################
function f_return=lookback_option(S0,K,r,delta,sigma,T,set_points)
   N=length(set_points(:,1));
	m=length(set_points(1,:));
   v_valor=zeros(N,1);
   for num_punto=1:N-1
     #Condicion para descargar el cero vector de un punto
	  vector_precios=zeros(m+1,1);
     vector_precios(1)=S0;
	  
	  if(sum(set_points(num_punto,:)>0)==m)

		 Z=stdnormal_inv(set_points(num_punto,:));		 
	    for num_periodo=1:m
         aux1 = exp (( r - delta - 0.5 * sigma * sigma) * T/m);
         aux2 = exp ( sigma * sqrt(T/m) * Z(num_periodo));
			vector_precios(num_periodo+1)=vector_precios(num_periodo)*aux1*aux2;
		 endfor

	  endif
     # Lookback max(max(S0,S1,...,Sm)-K,0)
     maximo=max(max(S0,max(vector_precios))-K,0);
     v_valor(num_punto)=maximo;
	endfor
   f_return=exp(-r*T)*mean(v_valor);
endfunction
