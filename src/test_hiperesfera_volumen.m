# Calcula el volumen exacto de una n-esfera
# usando método MC
# INPUTS
# dim : dimensión del espacio
# R : radio de la esferea
# Formula exacta Vn= pi^n/2 * R^n / gamma(n/2+1)

dim=8; %dimension
R=1; %radio

muestramax=30000;

vol_teorico=f_hiperesfera_volumen(dim,R);
volumen_estimado=eye(muestramax,1);
errores_mc=eye(muestramax,1);

elapse_time=0;
t0=clock();
num_puntos_dentro_esfera=0;
for i=1:muestramax

	punto_aleat=f_hipercubo_punto_aleatorio(dim,R);
	if(f_hiperesfera_dentro_radio(R,punto_aleat)==true);
	  num_puntos_dentro_esfera+=1; 
	endif

	est_vol_mc(i)=(num_puntos_dentro_esfera/i)*R*power(2,dim);;

endfor
elapse_time=etime(clock(),t0)
volumen_teorico=f_hiperesfera_volumen(dim,R)
volumen_estimado_mc=est_vol_mc(muestramax)

#x=500:muestramax;
#est_vol1=est_vol(500:muestramax);
#plot(x,est_vol1,'k');

%Halton
#v=[2,3,5,7,13,17,19,23,27,31];
v=[2,3,5,7,13,17,19,23];
#v=[2,3,5,7,13];
#v=[2,3,5];

u=f_halton(v,muestramax);
num_puntos_dentro_esfera=0;
for i=1:muestramax
   punto_halton=u(i,:);
	if(f_hiperesfera_dentro_radio(R,punto_halton)==true);
	  num_puntos_dentro_esfera+=1; 
	endif
	est_vol_halton(i)=(num_puntos_dentro_esfera/i)*R*power(2,dim);;
endfor
volulem_estimado_halton=est_vol_halton(muestramax)



plot(est_vol_mc(300:muestramax),'r',est_vol_halton(300:muestramax),'b');