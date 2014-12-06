
# INPUTS
# t : variable de la funcion
# parametro : permite elegir entre tipo de periodizacion
#parametro,modelo
#(1,poly-2),(2,poly-3),(3,poly-4),(4,sin-1),(5,sin-2),(6,sin-3),(7,sin-4),(8,noperio)
# OUTPUT
# Valor de la funcion transformada por la funcion elegida por parametro
function f_return=f_periodifica(t,parametro)
     #transformaciones polinomicas
	  if(parametro==1)
			f_return= 3 * power(t,2) - 2 * power(t,3); %TODO: extraer funciones
	  else if(parametro==2)
			f_return= 10 * power(t,3)- 15 * power(t,4) + 6 * power(t,5); 
	  else if(parametro==3)
			f_return= 35 * power(t,4)-84 * power(t,5) + 70 * power(t,6) - 20 * power(t,7); 
     endif
     endif
     endif
     #transformaciones trigonometricas
	  if(parametro==4) 
		   f_return = 1 / 2 * ( 1 - cos( pi * t ) ); 
	  else if(parametro==5)
			f_return = ( 1 / ( 2 * pi ) ) * ( 2 * pi * t - sin ( 2 * pi * t ) ); 
	  else if(parametro==6)
			f_return = ( 1 / 16 ) * ( 8 - 9 * cos ( pi * t ) + cos( 3 * pi * t ) ); 
	  else if(parametro==7)
			f_return = ( 1 / ( 12 * pi ) ) * ( 12 * pi * t - 8 * sin( 2 * pi * t ) + sin ( 4 * pi * t ) );
     endif
     endif
	  endif
     endif

     #No periodifica
	  if(parametro==8)
			 f_return=t;
     endif

endfunction
