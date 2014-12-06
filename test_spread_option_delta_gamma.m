# TEST SPREAD OPTIONS:  Calculo de griegas Delta y Gamma
# INPUTS
# w1 y w2 : pesos de cada subyacente considerados positivos
# rate : tipo de interes
# delta1 y delta2 : dividendos para los subyacente 1 y 2
# S01 y S02 precios de los subyacente en el instante 0
# sigma1 y sigma2 son las volatilidades de los subyacentes
# ro12 en [-1,1] correlación entre los subyacentes
# T tiempo de madurez de las opciones
# K precio del strike del spread
# param : tipo de periodizacion aplicada
# OUTPUTS
# Valor de la griega delta1, delta2, gamma1 y gamma2 para una Spread Option

#Parametros fijos
w1=w2=1;
S20=100;
delta1=0.05;
delta2=0.05;
sigma1=0.3;
sigma2=0.2;
ro12=0.5;
rate=0.05;
T=5;
K=4;

printf("PARAMETROS DE LA SIMULACION\n");
printf("w1: %.2f \nw2: %.2f \n",w1,w2)
printf("S20: %.2f \n",S20);
printf("delta1: %.2f \ndelta2: %.2f \n",delta1,delta2);
printf("sigma1: %.2f \nsigma2: %.2f \n",sigma1,sigma2);
printf("ro12: %.2f \n",ro12);
printf("rate: %.2f \n",rate);
printf("T: %.2f \nK: %.2f \n",T,K);

# casos de periodizacion
# (1,poly-2),(2,poly-3),(3,poly-4),(4,sin-1),(5,sin-2),(6,sin-3),(7,sin-4),(8,noperio)
array_param_perio=1:8; # poly-3, sin-2, sin-3

# casos de precios para S10
array_S10 = [95,96,97,98,99,100,101,102,103,104];
DELTA1    = zeros(length(array_S10),length(array_param_perio));
DELTA2    = zeros(length(array_S10),length(array_param_perio));
GAMMA1    = zeros(length(array_S10),length(array_param_perio));
GAMMA2    = zeros(length(array_S10),length(array_param_perio));

errorstandardDELTA1    = zeros(length(array_S10),length(array_param_perio));
errorstandardDELTA2    = zeros(length(array_S10),length(array_param_perio));
errorstandardGAMMA1    = zeros(length(array_S10),length(array_param_perio));
errorstandardGAMMA2    = zeros(length(array_S10),length(array_param_perio));


##############################
# CASOS N=55(m=10),233(m=13) #
##############################
array_fibo=[13]; #casos para glp fibonaci

for tamfibo=1:length(array_fibo)
# creamos el conjunto de puntos glp
  m=array_fibo(tamfibo);

  printf("---------------------------------\n");
  printf("NUMERO PUNTOS good lattice points: %d\n",length(glp));
  printf("---------------------------------\n");

  for precioS10=1:length(array_S10)
    S10=array_S10(precioS10);
    printf("----------\n");
	 printf("Precio S10: %d\n",S10);
    printf("----------\n");
    for perio_param=1:length(array_param_perio)
      printf("-------------\n");
	   printf("Periodizacion: %d\n",perio_param);
      printf("-------------\n");
 
      parametro_periodizacion=array_param_perio(perio_param);

      glp=f_glp(m);
      muestras=10;
		teta=zeros(muestras,1);

      #Se generan desplazamiento del gpl para estimar el error standard
		elapse_time_delta1=0;
		sumestimaciones=0;
      for k=1:muestras
		    glpshift=f_random_shift_set(glp);
			 t0=clock();
	       teta(k)=spread_option_delta1_perio(glpshift,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,parametro_periodizacion);
			 elapse_time_delta1+=etime(clock(),t0)/muestras;
			 sumestimaciones+=teta(k);
		endfor

		DELTA1(precioS10,perio_param)=sumestimaciones/muestras;
		errorstandardDELTA1(precioS10,perio_param)=log(error_standard(teta));

      #Se generan desplazamiento del gpl para estimar el error standard
		elapse_time_gamma1=0;
		sumestimaciones=0;
      for k=1:muestras
		    glpshift=f_random_shift_set(glp);
			 t0=clock();
	       teta(k)=spread_option_gamma1_perio(glpshift,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,parametro_periodizacion);
			 elapse_time_gamma1+=etime(clock(),t0)/muestras;
			 sumestimaciones+=teta(k);
		endfor

		GAMMA1(precioS10,perio_param)=sumestimaciones/muestras;
		errorstandardGAMMA1(precioS10,perio_param)=log(error_standard(teta));

      #Se generan desplazamiento del gpl para estimar el error standard
		elapse_time_delta2=0;
		sumestimaciones=0;
      for k=1:muestras
		    glpshift=f_random_shift_set(glp);
			 t0=clock();
	       teta(k)=spread_option_delta2_perio(glpshift,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,parametro_periodizacion);
			 elapse_time_delta2+=etime(clock(),t0)/muestras;
			 sumestimaciones+=teta(k);
		endfor

		DELTA2(precioS10,perio_param)=sumestimaciones/muestras;
		errorstandardDELTA2(precioS10,perio_param)=log(error_standard(teta));

      #Se generan desplazamiento del gpl para estimar el error standard
		elapse_time_gamma2=0;
		sumestimaciones=0;
      for k=1:muestras
		    glpshift=f_random_shift_set(glp);
			 t0=clock();
	       teta(k)=spread_option_gamma2_perio(glpshift,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,parametro_periodizacion);
			 elapse_time_gamma2+=etime(clock(),t0)/muestras;
			 sumestimaciones+=teta(k);
		endfor

		GAMMA2(precioS10,perio_param)=sumestimaciones/muestras;
		errorstandardGAMMA2(precioS10,perio_param)=log(error_standard(teta));


    endfor
  endfor
endfor

printf("simulacion terminada con exito :) \n");



