% INPUT 
% n dimensión del espacio
% R radio hipercubo

% OUTPUT: punto aleatorio en el hipercubo de dimension n y radio R
function f_retorno=f_hipercubo_punto_aleatorio(n,R)

   x=eye(n,1);
   for i=1:n
	  x(i)=rand*R;
	endfor

	f_retorno=x;

endfunction
