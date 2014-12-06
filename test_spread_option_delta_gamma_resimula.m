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

# periodizacion sin-2
param=2; 
# N=55
m=10;    
glp=f_glp(m);
# Precio
S10=96;
# Variacion del precio
h=0.0000001;  #10e-7
# Iteraciones glp
iter=10;  # N=55,89,144,233,377,610,987,1597,2584,4181

elapse_time=eye(iter,2);
lenglp=eye(iter,1);

for i=1:iter
  #generar GLM con m
  glp=f_glp(m);
  lenglp(i)=length(glp);
  m+=1;
  #METODO DIRECTO
  t0=clock();
  delta_met_dir=spread_option_delta1_perio(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,param);
  delta_met_dir
  elapse_time(i,1)=etime(clock(),t0);
  #METODO DE RESIMULACION
  t0=clock();
  valor            = spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,param);
  valor_perturbado = spread_option_periodifica(glp,w1,w2,rate,K,S10+h,S20,delta1,delta2,sigma1,sigma2,ro12,T,param);
  delta_met_resim=(valor_perturbado-valor)/h;
  delta_met_resim
  elapse_time(i,2)=etime(clock(),t0);

  diff=delta_met_resim-delta_met_dir
endfor
