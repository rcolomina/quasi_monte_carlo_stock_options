# INPUT  : Vector de estimaciones de la media
# OUTPUT : Error estandar de la media

function f_return=standard_error(vector)
		 f_return = std(vector) / sqrt(length(vector));
endfunction
