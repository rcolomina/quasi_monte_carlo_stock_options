% INPUTS
% dim : dimension del espacio
% radio : radio de la esfera
% muestras: numero de muestras
% OUTPUT
function f_retorno=f_volumen_hiperesfera_mc(dim,radio,muestras)

		 volumen=0;
		 for i=1:muestras
			punto=f_hipercubo_punto_aleatorio(dim);
			if(f_hiperesfera_dentro_radio(dim,radio,punto)==1);
			  volumen=volumen+1;
			endif
		 endfor
		 
		 volumen=volumen/muestras;
		 f_retorno=volumen*power(2*radio,dim);
endfunction
