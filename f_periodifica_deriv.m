# FUNCIONES DE PERIODIZACION POLINOMICAS Y TRIGONOMETRICAS
# INPUT
# t : variable de la funcion 
# parametro : tipo de transformada elegida
# OUTPUT
# Devuelve la variable transformada por la funcion elegida por parametro
function f_return=f_periodifica_deriv(t,parametro)
#parametro,modelo
#(1,poly-2),(2,poly-3),(3,poly-4),(4,sin-1),(5,sin-2),(6,sin-3),(7,sin-4),(8,noperio)

      #transformaciones polinomicas
	   if(parametro==1)
			f_return=6*power(t,1)-6*power(t,2); 
	   else if(parametro==2)
			f_return=30*power(t,2)-60*power(t,3)+30*power(t,4); 
	   else if(parametro==3)
			f_return=140*power(t,3)-420*power(t,4)+420*power(t,5)-140*power(t,6); 
		else
      #transformaciones polinomicas
	   if(parametro==4)
			f_return=pi/2*(sin(pi*t));
	   else if(parametro==5)
		 	f_return=1-cos(2*pi*t);
  	   else if(parametro==6)
		   f_return=1/16*(9*pi*sin(pi*t)-3*pi*sin(3*pi*t));
		else if(parametro==7)
		   f_return=(1/(12*pi))*(12*pi-16*pi*cos(2*pi*t)+4*pi*cos(4*pi*t));
      #no transfoma
		else if(parametro==8)
			f_return=1;
      endif
		endif
		endif
		endif
		endif
		endif
		endif
      endif

endfunction
