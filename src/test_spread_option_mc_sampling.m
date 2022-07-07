#pesos de la spread option
w1=w2=1;

##Primera pata
S10=100;
delta1=0.05;
sigma1=0.3;

##segunda
#S20=110;
#delta2=0.05;
#sigma2=0.2;

##entorno 
#ro12=0.8;
#rate=0.0;
K=0;
#T=1;
#Numero de pruebas o iteraciones: iter
iter=1;
error=1:iter;
vectorN=1:iter;
for k=1:iter
  random_uniform_set;#genera nuestra rejilla buena de puntos
  errorsum=0; #reseteamos el error
  numopc=5;  #numero de opciones de ensayo
  for numero=1:numopc
     #aleatorizar la segunda pata 
     S20=unifrnd(50,130);
     T=unifrnd(0.5,1);
	  sigma2=unifrnd(0.1,0.5);
	  delta2=unifrnd(0.01,0.1);
     ro12=unifrnd(-0.8,0.8);
     rate=unifrnd(0.01,0.15);

     mc=spread_option(rndunifset,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);
     mf=margrabe_formula(S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);

     errorsum=errorsum+((mc-mf)/mf)*((mc-mf)/mf);
   endfor

   error(k)=sqrt(errorsum/numopc)*100;
   #vectorN(k)=N;

endfor
plot(error,"*");
