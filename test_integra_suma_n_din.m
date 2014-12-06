# Calcular la integral seno (X+...Xs) 
# sobre [0,1)^s
# usando método MC y QMC
# INPUTS
# dim : dimensión del espacio
# 


dim=2; %dimension
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

#	sumaparcial*=pi;
 
#   if(i==1)
#      sumatorio(i)=sin(sumaparcial);
#   else
#      sumatorio(i)=sumatorio(i-1)+sin(sumaparcial);
#   endif
#	est_vol_mc(i)=(sumatorio(i)/i);

   if(i==1)
      sumatorio(i)=sumaparcial;
   else
      sumatorio(i)=sumatorio(i-1)+sumaparcial;
   endif

	est_vol_mc(i)=(sumatorio(i)/i);


endfor
elapse_time=etime(clock(),t0)

#volumen_estimado_mc=est_vol_mc(muestramax)

#x=500:muestramax;
#est_vol1=est_vol(500:muestramax);
#plot(x,est_vol1,'k');

%Halton
#v=[2,3,5,7,13,17,19,23,27,31];
#=[2,3,5,7,13,17,19,23];
#v=[2,3,5,7,13];
#v=[2,3,5];
v=[2,3];

punto_halton=f_halton(v,muestramax);
sumatorio=eye(muestramax,1);
for i=1:muestramax


   sumaparcial=sum(punto_halton(i,:));

#	sumaparcial*=pi;

   if(i==1)
      sumatorio(i)=sumaparcial;
   else
      sumatorio(i)=sumatorio(i-1)+sumaparcial;
   endif

 
#   if(i==1)
#      sumatorio(i)=sin(sumaparcial);
#   else
#      sumatorio(i)=sumatorio(i-1)+sin(sumaparcial);
#   endif


	est_vol_halton(i)=(sumatorio(i)/i);

endfor

plot(est_vol_mc(300:muestramax),'r',est_vol_halton(300:muestramax),'b');

#plot(est_vol_halton(300:muestramax),'b');
