% INPUTS
% dim : dimension del espacio
% radio : radio de la esfera
% m: puntos por dimension (total puntos 
% OUTPUT
% volumen hiperesfera

m=800;
radio=1;
dim=3;
totvol=0;

elapse_time=0;
t0=clock();
for i=1:m
	 for j=1:m 
					x=[(i/m)*radio,(j/m)*radio];
					valorf=f_hiperesfera_explicita_exacta(x,radio);
					difvol=power(radio/m,dim-1);
					totvol+=valorf*difvol;
    endfor
endfor
elapse_time=etime(clock(),t0);


volaproxima=totvol*power(2,dim)
volexacto=f_hiperesfera_volumen(dim,radio)