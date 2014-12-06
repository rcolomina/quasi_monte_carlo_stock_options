# NORMAL ESTANDAR INVERSA MODIFICADA
# INPUT
# x: percentil en el intervao (0,1)
# OUTPUT
# Inverso de la funcion de distribucion normal estandar
function f_ret=stdnormal_inv_modif(x)
	  if(x>0.999999999999999) 
			 f_ret=8.2095;
     else
			 if(x<0.00000000000001)
					f_ret=-8.2095;
          else
               f_ret=stdnormal_inv(x);
          endif
     endif
endfunction
