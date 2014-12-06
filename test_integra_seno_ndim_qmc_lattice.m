# Calcular la integral seno (X+...Xs) 
# sobre [0,1)^s
# usando método MC crudo y QMC(Lattice Rule Periodizacion)
# INPUTS
# dim : dimensión del espacio
# N : numero de puntos
# l : parametro de lattice rule rango 1
# OUTPUT
# Integral de función sen() por MC y QMC
dim=4;
N=100; 
l=19;
punto_lattice=eye(N,dim);
punto_lattice=f_glp_ndim(N,dim,l);
### Estimacion mediante MC crudo
elapse_time=0;
t0=clock();
sumatorio=eye(N,1);
for i=1:N
   #Funcion sin[pi*(x1+..+xs)]
   sumaparcial=0;
   for s=1:dim
     sumaparcial+=rand;
	endfor
	sumaparcial*=2*pi;
   if(i==1)
      sumatorio(i)=sin(sumaparcial);
   else
      sumatorio(i)=sumatorio(i-1)+sin(sumaparcial);
   endif
   #Aproximacion parcial
	est_vol_mc(i)=(sumatorio(i)/i);
endfor
elapse_time=etime(clock(),t0)
volumen_mc=est_vol_mc(N)
### Estimacion mediante QMC(Lattice)
sumatorio=eye(N,1);
for i=1:N
   #Funcion sin(pi*(sum(xi))
   sumaparcial=sum(punto_lattice(i,:));
	sumaparcial*=2*pi;
   if(i==1)
      sumatorio(i)=sin(sumaparcial);
   else
      sumatorio(i)=sumatorio(i-1)+sin(sumaparcial);
   endif
   #Aproximacion parcial
	est_vol_lattice(i)=(sumatorio(i)/i);
endfor
#Aproximacion total
volumen_qmc_lattice=est_vol_lattice(N)
#Grafica de la convergencia de MC y QMC
plot(est_vol_mc(1:N),'r',est_vol_lattice(1:N),'b');


