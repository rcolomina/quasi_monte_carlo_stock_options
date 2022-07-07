### CALCULA APROXIMACIONES DEL VALOR DE SPREAD OPTIONS PARA EL CASO GENERAL K igual a CERO
# INPUTS
# S10 : precio inicial primer activo
# delta1 : dividendos para el primer subyacente
# numopciones : numero de opciones a simular

# OUTPUTS
# Valoraciones de Spread Option para diferentes valores
# de tam. muestral y transformaciones de periodizacion

#Primera pata
S10=100;
delta1=0.05;
sigma1=0.3;

# entorno: Se fijan a precio de strike y pesos
# precio del ejercicio
K=0;
# pesos de la spread option
w1=w2=1;

#Segunda pata del Spread: generadas aleatoriamente
numopciones=50;
S20=1:numopciones;
T=1:numopciones;
sigma2=1:numopciones;
delta2=1:numopciones;
ro12=1:numopciones;
rate=1:numopciones;

#aleatorizar la segunda pata 
for j=1:numopciones
	  vS20(j)=unifrnd(50,130);
     vT(j)=unifrnd(0.5,1);
     vsigma2(j)=unifrnd(0.1,0.5);
     vdelta2(j)=unifrnd(0.01,0.1);
     vro12(j)=unifrnd(-0.8,0.8);
     vrate(j)=unifrnd(0.01,0.15);
endfor


#Numero de pruebas N=fibo(m)
iter=8;   #numero de pruebas para diferentes tamaños de glp
m=6;      #comenzamos con fibo(6) y terminamos con fibo(6+iter)
models=8; #modelos numericos

error=zeros(iter,models);
vector_N=zeros(1,iter);
for k=1:iter
  m=m+1;
  glp=f_glp(m);
  #calculamos un paquete de opciones 
  errorsum=zeros(1,models);
  mc=zeros(1,models);
  for numero=1:numopciones

     #colocamos los parametros a la segunda pata del spread
	  S20=vS20(numero);
     T=vT(numero);
	  sigma2=vsigma2(numero);
	  delta2=vdelta2(numero);
     ro12=vro12(numero);
     rate=vrate(numero);

     #Calculo de valor con modelo teorico
     mf=margrabe_formula(S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);

     #calculo con metodo numerico: Modelo poly-2
	  num_param_perio=1;
     mc1=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,num_param_perio);
     errorsum(num_param_perio)=errorsum(num_param_perio)+f_error(mc1,mf);

     #calculo con metodo numerico: Modelo poly-3
	  num_param_perio=2;
     mc2=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,num_param_perio);
     errorsum(num_param_perio)=errorsum(num_param_perio)+f_error(mc2,mf);

     #calculo con metodo numerico: Modelo poly-4
	  num_param_perio=3;
     mc3=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,num_param_perio);
     errorsum(num_param_perio)=errorsum(num_param_perio)+f_error(mc3,mf);

     #calculo con metodo numerico: Modelo sin 1-transform
	  num_param_perio=4;
     mc4=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,num_param_perio);
     errorsum(num_param_perio)=errorsum(num_param_perio)+f_error(mc4,mf);

     #calculo con metodo numerico: Model sin 2-transform
	  num_param_perio=5;
     mc5=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,num_param_perio);
     errorsum(num_param_perio)=errorsum(num_param_perio)+f_error(mc5,mf);

     #calculo con metodo numerico: Modelo sin 3-transform
	  num_param_perio=6;
     mc6=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,num_param_perio);
     errorsum(num_param_perio)=errorsum(num_param_perio)+f_error(mc6,mf);

     #calculo con metodo numerico: Modelo sin 4-transform
	  num_param_perio=7;
     mc7=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,num_param_perio);
     errorsum(num_param_perio)=errorsum(num_param_perio)+f_error(mc7,mf);

     #calculo con metodo numerico: No periodificado
	  num_param_perio=8;
     mc8=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,num_param_perio);
     errorsum(num_param_perio)=errorsum(num_param_perio)+f_error(mc8,mf);

   endfor

   error(k,1)=sqrt(errorsum(1)/numopciones)*100; #*100 para expresar en tanto por ciento
	error(k,2)=sqrt(errorsum(2)/numopciones)*100;
	error(k,3)=sqrt(errorsum(3)/numopciones)*100;
	error(k,4)=sqrt(errorsum(4)/numopciones)*100;
	error(k,5)=sqrt(errorsum(5)/numopciones)*100;
	error(k,6)=sqrt(errorsum(6)/numopciones)*100;
	error(k,7)=sqrt(errorsum(7)/numopciones)*100;
   error(k,8)=sqrt(errorsum(8)/numopciones)*100;

   vector_N(k)=fibo(m);
endfor

plot(log(vector_N),log(error(:,1)),"-o;Polynomial-2;",
     log(vector_N),log(error(:,2)),"-o;Polynomial-3;",
     log(vector_N),log(error(:,3)),"-o;Polynomial-4;",
     log(vector_N),log(error(:,4)),"-*;Sin1-Transform;",
     log(vector_N),log(error(:,5)),"-*;Sin2-Transform;",
     log(vector_N),log(error(:,6)),"-*;Sin3-Transform;",
     log(vector_N),log(error(:,7)),"-x;Sin4-Transform;",
     log(vector_N),log(error(:,8)),"-x;No Periodization;");

plot(log(vector_N),log(error(:,2)),"-o;Polynomial-3;",
     log(vector_N),log(error(:,3)),"-o;Polynomial-4;",     
     log(vector_N),log(error(:,6)),"-*;Sin3-Transform;",
     log(vector_N),log(error(:,7)),"-x;Sin4-Transform;",
     log(vector_N),log(error(:,8)),"-x;No Periodization;");

xlabel('Log(N)');
ylabel('Log(RMSE)');
