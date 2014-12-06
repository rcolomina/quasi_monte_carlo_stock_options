# Calcular la integral seno (X+...Xs) 
# sobre [0,1)^s
# usando método MC y QMC
# INPUTS
# dim : dimensión del espacio
# 

dim=4; #dimension
muestramax=5000;

#ol_teorico=f_hiperesfera_volumen(dim,R);

volumen_estimado=eye(muestramax,1);
#rrores_mc=eye(muestramax,1);

elapse_time=0;
t0=clock();
#um_puntos_dentro_esfera=0;
sumatorio=eye(muestramax,1);

for i=1:muestramax

   sumaparcial=0;
   for s=1:dim
     sumaparcial+=rand;
	endfor

	sumaparcial*=pi;
 
   if(i==1)
      sumatorio(i)=sin(sumaparcial);
   else
      sumatorio(i)=sumatorio(i-1)+sin(sumaparcial);
   endif
	est_vol_mc(i)=(sumatorio(i)/i);

endfor
elapse_time=etime(clock(),t0)

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


punto_halton=f_halton(v,muestramax);
sumatorio=eye(muestramax,1);
for i=1:muestramax


   sumaparcial=sum(punto_halton(i,:));
	sumaparcial*=pi;

   if(i==1)
      sumatorio(i)=sin(sumaparcial);
   else
      sumatorio(i)=sumatorio(i-1)+sin(sumaparcial);
   endif


	est_vol_halton(i)=(sumatorio(i)/i);

endfor
volumen_halton=est_vol_halton(muestramax)

plot(est_vol_mc(500:muestramax),'r',est_vol_halton(500:muestramax),'b');


