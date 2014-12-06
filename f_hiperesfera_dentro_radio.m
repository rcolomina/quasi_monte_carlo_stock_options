% INPUT 
% R radio
% x punto espacio de dimension n, n-componentes

% OUTPUT: 
% true si esta dentro, false fuera

function f_retorno=f_hiperesfera_dentro_radio(R,x)

   if((norm(x))<R)
	  f_retorno=true;
	else
	  f_retorno=false;
   endif
endfunction