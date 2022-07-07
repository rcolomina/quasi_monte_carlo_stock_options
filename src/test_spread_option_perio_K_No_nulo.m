#pesos de la spread option
#Primera pata
S10=100;
delta1=0.05;
sigma1=0.3;

#entorno 
K=4;
w1=w2=1;

#Segunda pata del Spread
numopciones=50;
S20=1:numopciones;
T=1:numopciones;
sigma2=1:numopciones;
delta2=1:numopciones;
ro12=1:numopciones;
rate=1:numopciones;

#Aleatorizar la segunda pata 
for j=1:numopciones
	  vS20(j)=unifrnd(50,130);
     vT(j)=unifrnd(0.5,1);
     vsigma2(j)=unifrnd(0.1,0.5);
     vdelta2(j)=unifrnd(0.01,0.1);
     vro12(j)=unifrnd(-0.8,0.8);
     vrate(j)=unifrnd(0.01,0.15);
endfor


#Numero de pruebas N=fibo(m)
iter=10;  #numero de pruebas para diferentes t
m=6;      #comenzamos con fibo(6) y terminamos con fibo(6+iter)
models=8; #modelos numericos

error=zeros(iter,models);
vector_N=zeros(1,iter);
for k=1:iter
  m=m+1;
  good_lattice_points;
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

     for model=1:models
   	  num_param_perio=model;
        mc=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,num_param_perio);
        errorsum(num_param_perio)=errorsum(num_param_perio)+f_error(mc,mf);
     endfor


   endfor


   error(k,1)=sqrt(errorsum(1)/numopciones)*100;
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
