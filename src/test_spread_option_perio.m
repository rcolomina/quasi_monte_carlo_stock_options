#pesos de la spread option
#Primera pata
S10=100;
delta1=0.05;
sigma1=0.3;

#entorno 
K=0;
#rate=0;
w1=w2=1;

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
     #aleatorizar la segunda pata 
     S20=unifrnd(50,130);
     T=unifrnd(0.5,1);
	  sigma2=unifrnd(0.1,0.5);
	  delta2=unifrnd(0.01,0.1);
     ro12=unifrnd(-0.8,0.8);
     rate=unifrnd(0.01,0.15);

     mc=spread_option_perio(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);
     mf=margrabe_formula(S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);

     errorsum=errorsum+((mc-mf)/mf)*((mc-mf)/mf);
   endfor

   error(k)=sqrt(errorsum/numopc)*100;
   vector_N(k)=fibo(m);

endfor

plot(error,"*");
