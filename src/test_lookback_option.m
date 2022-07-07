# INPUTS
# N : numero de puntos de la red de integracion
# param : parametro de Lattice Rule rango 1
# v_halton : vector de primos para suc. halton
# Precios de una Lookback Call Option basado en
# Monte Carlo, GLP y GLP+Periodizacion

#Parametros de lso métodos
N=1024;
param=363;

%N=512;#1024;
%param=151;#363;

v_halton=[2,3,5,7,11];
pruebas=10;
dim=5;

param_perio=3;

#Parametros de la opcion
S0=100;
K=120
r=0.1;
delta=0;
sigma=0.2;
T=5;

# Test
mc=0;
qmchib=0;
qmchalton=0;
qmcglp=1;
qmcglpper=1;


#MONTE CARLO CRUDO
if(mc==true)
vec_val_lb=zeros(pruebas,1);
for i=1:pruebas
   set_puntos=rand(N,dim);
   vec_val_lb(i)=lookback_option(S0,K,r,delta,sigma,T,set_puntos);
endfor
valor_lookback_mc=mean(vec_val_lb)
desviacion_estandard=standard_error(vec_val_lb)
printf("------------------\n");
endif


#QMC - HIBRIDO USANDO VAN DER CORPUT N DIM
if(qmchib==true)
set_puntos=f_van_der_corput_ndim(N,dim);
for i=1:pruebas
  set_puntos_desplazados=f_random_shift_ndim_set(set_puntos);
  valor_lookback_qmc_hibrido_vandercorput(i)=lookback_option(S0,K,r,delta,sigma,T,set_puntos_desplazados);
endfor
val_lookback_qmc_hibrido_vandercorput=mean(valor_lookback_qmc_hibrido_vandercorput)
est_error_val_lookback_qmc_hibrido_vandercorput=standard_error(valor_lookback_qmc_hibrido_vandercorput)
printf("------------------\n");
endif

#QMC - HALTON
if(qmchalton==true)
set_puntos=f_halton(v_halton,N);
for i=1:pruebas
  set_puntos_desplazados=f_random_shift_ndim_set(set_puntos);
  valor_lookback_qmc_halton(i)=lookback_option(S0,K,r,delta,sigma,T,set_puntos_desplazados);
endfor
val_lookback_qmc_halton=mean(valor_lookback_qmc_halton)
est_error_val_lookback_qmc_halton=standard_error(valor_lookback_qmc_halton)
printf("------------------\n");
endif

#QMC - GOOD LATTICE POINTS
if(qmcglp==true)
set_puntos=f_glp_ndim(N,dim,param);
for i=1:pruebas
  set_puntos_desplazados=f_random_shift_ndim_set(set_puntos);
  valor_lookback_qmc_lr(i)=lookback_option(S0,K,r,delta,sigma,T,set_puntos_desplazados);
endfor
val_lookback_qmc_lr=mean(valor_lookback_qmc_lr)
est_error_val_lookback_qmc_lr=standard_error(valor_lookback_qmc_lr)
printf("------------------\n");
endif

#QMC - GOOD LATTICE POINTS (Periodizacion)
if(qmcglpper==true)
vparam=[1,2,4,5];
for param_perio=1:length(vparam)


  param_perio=1

  set_puntos=f_glp_ndim(N,dim,param);
  for i=1:pruebas
	 set_puntos_desplazados=f_random_shift_ndim_set(set_puntos);
	 valor_lookback_qmc_lr_perio(i)=lookback_option_periodiza(S0,K,r,delta,sigma,T,set_puntos_desplazados,param_perio);
  endfor
  val_lookback_qmc_lr_perio=mean(valor_lookback_qmc_lr_perio)
  est_error_val_lookback_qmc_lr_perio=standard_error(valor_lookback_qmc_lr_perio)
  endif
endfor

#QMC - GOOD LATTICE POINTS (Periodizacion)
param_perio=2
if(qmcglpper==true)
set_puntos=f_glp_ndim(N,dim,param);
for i=1:pruebas
  set_puntos_desplazados=f_random_shift_ndim_set(set_puntos);
  valor_lookback_qmc_lr_perio(i)=lookback_option_periodiza(S0,K,r,delta,sigma,T,set_puntos_desplazados,param_perio);
endfor
val_lookback_qmc_lr_perio=mean(valor_lookback_qmc_lr_perio)
est_error_val_lookback_qmc_lr_perio=standard_error(valor_lookback_qmc_lr_perio)
endif

#QMC - GOOD LATTICE POINTS (Periodizacion)
if(qmcglpper==true)
param_perio=4
set_puntos=f_glp_ndim(N,dim,param);
for i=1:pruebas
  set_puntos_desplazados=f_random_shift_ndim_set(set_puntos);
  valor_lookback_qmc_lr_perio(i)=lookback_option_periodiza(S0,K,r,delta,sigma,T,set_puntos_desplazados,param_perio);
endfor
val_lookback_qmc_lr_perio=mean(valor_lookback_qmc_lr_perio)
est_error_val_lookback_qmc_lr_perio=standard_error(valor_lookback_qmc_lr_perio)
endif

#QMC - GOOD LATTICE POINTS (Periodizacion)
if(qmcglpper==true)
param_perio=5
set_puntos=f_glp_ndim(N,dim,param);
for i=1:pruebas
  set_puntos_desplazados=f_random_shift_ndim_set(set_puntos);
  valor_lookback_qmc_lr_perio(i)=lookback_option_periodiza(S0,K,r,delta,sigma,T,set_puntos_desplazados,param_perio);
endfor
val_lookback_qmc_lr_perio=mean(valor_lookback_qmc_lr_perio)
est_error_val_lookback_qmc_lr_perio=standard_error(valor_lookback_qmc_lr_perio)
endif


#Resultados
#mSalida=zeros(5,2);

#mSalida(1,1)=valor_lookback_mc;
#mSalida(1,2)=desviacion_estandard;

#mSalida(2,1)=val_lookback_qmc_hibrido_vandercorput;
#mSalida(2,2)=est_error_val_lookback_qmc_hibrido_vandercorput;

#mSalida(3,1)=val_lookback_qmc_halton;
#mSalida(3,2)=est_error_val_lookback_qmc_halton;

#mSalida(4,1)=val_lookback_qmc_lr;
#mSalida(4,2)=est_error_val_lookback_qmc_lr;

#mSalida(5,1)=val_lookback_qmc_lr_perio;
#mSalida(5,2)=est_error_val_lookback_qmc_lr_perio;


