#pesos de la spread option
#Primera pata
S10=100;
delta1=0.05;
sigma1=0.3;

#entorno 
K=0;
#rate=0;
w1=w2=1;

#Segunda pata del Spread
S20=1:50;
T=1:50;
sigma2=1:50;
delta2=1:50;
ro12=1:50;
rate=1:50;

#aleatorizar la segunda pata 
numopciones=50;
for j=1:numopciones
	  vS20(j)=unifrnd(50,130);
     vT(j)=unifrnd(0.5,1);
     vsigma2(j)=unifrnd(0.1,0.5);
     vdelta2(j)=unifrnd(0.01,0.1);
     vro12(j)=unifrnd(-0.8,0.8);
     vrate(j)=unifrnd(0.01,0.15);
endfor


#Numero de pruebas N=fibo(m)
iter=10;
error=1:iter;
vector_N=1:iter;
m=6; #comenzamos con fibo(6) y terminamos con fibo(6+iter)
for k=1:iter
  m=m+1;
  good_lattice_points;
  #calculamos un paquete de opciones 
  errorsum=0;
  numopc=50;
  for numero=1:numopc

	  S20=vS20(numero);
     T=vT(numero);
	  sigma2=vsigma2(numero);
	  delta2=vdelta2(numero);
     ro12=vro12(numero);
     rate=vrate(numero);

     mc=spread_option_perio(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);
     mf=margrabe_formula(S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);

     errorsum=errorsum+((mc-mf)/mf)*((mc-mf)/mf);
   endfor

   error(k)=sqrt(errorsum/numopc)*100;
   vector_N(k)=fibo(m);

endfor

plot(log(error),"-@");
