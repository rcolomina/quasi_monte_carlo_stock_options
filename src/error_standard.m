# Rutina que calcular el error estandar para un vector de estimaciones

# INPUT:  Vector de estimaciones
# OUTPUT: Error standard

function f_ret=error_standard(vector_estimador)
	  len=length(vector_estimador);
	  media=0;
	  #estimador de la media
	  media=mean(vector_estimador);

     sumerror=0;
	  #error standard
	  for i=1:len
		  a1=vector_estimador(i)-media;
		  alfa=a1*a1;
		  sumerror=sumerror+alfa;
	  endfor
	  f_ret=sqrt((len-1)/len*sumerror);	 
endfunction
