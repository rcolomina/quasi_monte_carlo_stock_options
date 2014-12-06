% INPUT 
% n dimensión del espacio
% R radio

% OUTPUT: volumen exacto de la hiperesfera

function f_retorno=f_hiperesfera_volumen(n,R)
	f_retorno = power(pi,n/2)*power(R,n)/gamma(n/2+1);
endfunction
