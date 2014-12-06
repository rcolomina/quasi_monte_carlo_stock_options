%Parametros 
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

array_param_perio=[2;5;6]; % poly-3, sin-2, sin-3
array_S10=[96;100;104];

%%%%%%%%%%%%%%%
% CASO N=55
%%%%%%%%%%%%%%%
m=10; %variable para el script siguiente
good_lattice_points; %generamos la variable glp  %TODO cambiar script a funcion
length(glp)

for precioS10=1:length(array_S10)
  S10=array_S10(precioS10)
  for perio_param=1:length(array_param_perio)
	 printf("Periodizacion %d:\n",perio_param);
    parametro_periodizacion=array_param_perio(perio_param);
	 DELTA1=spread_option_delta1_perio(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,parametro_periodizacion);
	 DELTA1
	 DELTA2=spread_option_delta2_perio(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,parametro_periodizacion);
	 DELTA2

  endfor
endfor

%%%%%%%%%%%%%%%%
% CASO N=233
%%%%%%%%%%%%%%%
m=13; %variable para el script siguiente
good_lattice_points; %generamos la variable glp  %TODO cambiar script a funcion
length(glp)

for precioS10=1:length(array_S10)
  S10=array_S10(precioS10)
  for perio_param=1:length(array_param_perio)
	 printf("Periodizacion %d:\n",perio_param);
    parametro_periodizacion=array_param_perio(perio_param);
	 DELTA1=spread_option_delta1_perio(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,parametro_periodizacion);
	 DELTA1

	 DELTA2=spread_option_delta2_perio(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,parametro_periodizacion);
	 DELTA2

  endfor
endfor


