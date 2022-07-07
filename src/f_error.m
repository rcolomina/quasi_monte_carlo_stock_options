#INPUT : 
# Valor de una estimacion : estimado 
# Valor teorico : teorico
#OUTPUT: 
#Error cuadrático relativo al valor teórico 

function f_ret=f_error(estimado,teorico)

	  f_ret=power(((teorico-estimado)/teorico),2);

endfunction
