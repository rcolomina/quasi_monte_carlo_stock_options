# Calcular la integral seno (X1+...XS) 
# sobre [0,1)^s
# usando método MC y QMC
# INPUTS
# dim : dimensión del espacio
# muestramax : Numero de muestras
# OUTPUt
# Valor integral proximo a cero 

%for j=1:6
%vdim=[4,7,10,13,20,40];
dim=100;
%dim=vdim(j)
muestramax=50000;

### Estimacion mediante QMC(Halton)
if(dim==4)
  v=[2,3,5,7];  
else if(dim==7)
  v=[2,3,5,7,11,13,17];
else if(dim==10)
  v=[2,3,5,7,11,13,17,19,23,29];
else if(dim==13)
  v=[2,3,5,7,11,13,17,19,23,29,31,37,41];
else if(dim==20)
  v=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71];
else if(dim==40)
  v=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173];
else if(dim==100)
  v=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541];
endif 
endif
endif
endif
endif
endif
endif

#Reservar memoria
volumen_estimado=eye(muestramax,1);
sumatorio=eye(muestramax,1);
est_vol_halton=eye(muestramax,1);
est_vol_halton=eye(muestramax,1);


# Calculo mediante MC
t0=clock();
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
elapse_time_MC=etime(clock(),t0)
estamacion_mc=est_vol_mc(muestramax)


# Calculo mediante QMC(Halton)
t1=clock();
sumatorio=eye(muestramax,1);
punto_halton=f_halton(v,muestramax);
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
elapse_time_QMC_halton=etime(clock(),t1)
estamacion_qmc_halton=est_vol_halton(muestramax)

#plot(est_vol_mc(500:muestramax),'r',est_vol_halton(500:muestramax),'b');

#endfor
