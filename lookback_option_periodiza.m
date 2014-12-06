##############################################
# Autor   : Ruben Colomina Citoler
# Fecha   : 30-08-2013
##############################################
# INPUTS
# S0 : precio de arranque del subyacente
# K : precio del strike 
# r : tipo de interes
# delta : dividendo del subyacente
# sigma : volatilidad
# T : periodo de maduracion de la opcion
# set_points : conjunto de puntos de Nxm
#  siendo N numero de puntos y m la dimension
#  en [0,1)^m
# param_perio : parametro de periodizacion
#        
##############################################
# OUTPUT
# Valoracion de una opcion lookback discreta
##############################################
function f_return=lookback_option_periodiza(S0,K,r,delta,sigma,T,set_points,param_perio)

   N=length(set_points(:,1));
	m=length(set_points(1,:));

   aux1 = exp (( r - delta - 0.5 * sigma * sigma) * T/m);

   %Acota valores en entrada
   coordmin=0.000000000000000001; %10e-8
   coordmax=0.999999999999999999; %1-10e-8

   sumaZ=0;
   sumaMax=0;

   v_valor=zeros(N-1,1);
   for num_punto=1:N-1
     #Condicion para descargar el cero vector de un punto
	  vector_precios=zeros(m+1,1);
     vector_precios(1)=S0;
     #Coeficiente de periodizacion multiplica al integrando
     coef_perio_dif=1; 

     #Transformar el conjunto a normal estandard
  	  %puntos_perio=set_points(num_punto,:);
	  puntos_perio=f_periodifica(set_points(num_punto,:),param_perio);

	  #Z=zeros(m,1);
	  #Z=stdnormal_inv(puntos_perio);
     #Z=stdnormal_inv_modif(puntos_perio);	   

	  #Inversion por Acklam
	  for i=1:m

       coordenada_modif=puntos_perio(i);
		 if(puntos_perio(i)<coordmin)
		   coordenada_modif=coordmin;
		 else if(puntos_perio(i)>coordmax)
		   coordenada_modif=coordmax;
	    endif
		 endif
	    Z(i)=stdnormal_inv_acklam(coordenada_modif);
	  endfor

     #Calcular coeficiente de periodizacion 
	  for coord=1:m
		 valor_coord=set_points(num_punto,coord);
	  	 coef_perio_dif=coef_perio_dif*f_periodifica_deriv(valor_coord,param_perio);
	  endfor
	 
     vector_precios(1)=S0;
	  for num_periodo=1:m
  
		   if(Z(num_periodo)>10000)
			  Z(num_periodo)
			end

         aux2 = exp ( sigma * sqrt(T/m) * Z(num_periodo) );

			if(aux2>10000)
			  aux2
			end

			valor=vector_precios(num_periodo)*aux1*aux2;

			if(valor>10000)
			  valor
			endif

			vector_precios(num_periodo+1)=valor;
	  endfor		 

     # Lookback max(max(S0,S1,...,Sm)-K,0)
     maximo=max(max(S0,max(vector_precios))-K,0);
     #sumaMax=sumaMax+maximo;
     v_valor(num_punto)=maximo*coef_perio_dif;
	endfor
   %sumaMax
   %sumaZ

   f_return=exp(-r*T)*mean(v_valor);
endfunction
