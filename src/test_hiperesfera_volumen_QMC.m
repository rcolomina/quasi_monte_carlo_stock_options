# Calcula el volumen de una n-esfera
# usando método MC y QMC
# INPUTS
# dim : dimensión del espacio
# R : radio de la esferea
# nuestramax : Numero de muestras
# Formula exacta Vn= pi^n/2 * R^n / gamma(n/2+1)

dim=10; %dimension
R=1; %radio
muestramax=50000;

#Reservar memoria
volumen_estimado=eye(muestramax,1);
errores_mc=eye(muestramax,1);

### Estimacion mediante MC
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
volumen_estimado_mc=est_vol_mc(muestramax)

#Volumen exacto teorico
volumen_teorico=f_hiperesfera_volumen(dim,R)


### Estimacion mediante QMC(Halton)
if(dim==4)
  v=[2,3,5,7];  
else if(dim==7)
  v=[2,3,5,7,11,13,17];
else if(dim==10)
  v=[2,3,5,7,11,13,17,19,23,29];
else if(dim==13)
  v=[2,3,5,7,11,13,17,19,23,29,31,37,41];
endif
endif
endif
endif

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

plot(est_vol_mc(1000:muestramax),'r',est_vol_halton(1000:muestramax),'b');
