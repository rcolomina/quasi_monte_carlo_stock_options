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
rate=0.0;
K=0;
#T=1;

#Numero de pruebas iter
iter=10;
error=1:iter;
vectorN=1:iter;
m=6; #comenzamos con fibo(6)=13
for k=1:iter
  m=m+1; #input para el script good_lattice_points
  good_lattice_points;#genera nuestra rejilla buena de puntos
  errorsum=0; #reseteamos el error
  numopc=150;  #numero de opciones de ensayo
  for numero=1:numopc
     #aleatorizar la segunda pata 
     S20=unifrnd(50,130);
     T=unifrnd(0.5,1);
	  sigma2=unifrnd(0.1,0.5);
	  delta2=unifrnd(0.01,0.1);
     ro12=unifrnd(-0.8,0.8);
     rate=unifrnd(0.01,0.15);

     mc=spread_option(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);
     mf=exp(-rate*T)*margrabe_formula(S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);

     errorsum=errorsum+((mc-mf)/mf)*((mc-mf)/mf);
   endfor

   error(k)=sqrt(errorsum/numopc)*100;
   vectorN(k)=fibo(m);

endfor
plot(error,"*");
