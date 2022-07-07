% INPUTS
% dim : dimension del espacio
% radio : radio de la esfera
% muestras: numero de muestras
% OUTPUT
% volumen hiperesfera
function f_retorno=f_hiperesfera_volumen_mc(dim,radio,muestras)

		 volumen=0;
		 for i=1:muestras
			punto=f_hipercubo_punto_aleatorio(dim,radio);
			if(f_hiperesfera_dentro_radio(radio,punto)==true);
			  volumen+=1;
			endif
		 endfor
		 
		 volumen/=muestras;
		 f_retorno=volumen*power(2*radio,dim);
endfunction
