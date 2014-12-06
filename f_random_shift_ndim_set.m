# Desplazamiento aleatorio de los puntos del array
# modulo 1
#INPUTS: 
# Array multidimensional Nxs en [0,1)^s
#OUTPUTS: 
#Array multidimensional desplazado en [0,1)^s
function array_shifted_mod1=f_random_shift_ndim_set(array)

  dim=length(array(1,:));

  #crear vector de desplazamiento aleatorio
  vrand=rand;
  for i=2:dim
	 vrand=[vrand,rand];
  endfor
	
  #desplazar array de entrada y aplicar mod 1 
  for i=1:length(array(:,1))
     array_shifted(i,:)=array(i,:)+vrand;
  endfor

  array_shifted_mod1=fmod(array_shifted,1);	 

endfunction
