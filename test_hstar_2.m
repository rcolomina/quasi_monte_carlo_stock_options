
N=300;
w1=w2=1;
K=0;
S10=100;
sigma1=0.3;
delta1=0.05;

#fijar valores para la segunda pata de la spread
rate =  0.019441;
delta2 =  0.059396;
S20 =  52.720;
sigma2 =  0.16286;
ro12 = -0.77183;
T =  0.96923;

#fijar valores para la segunda pata de la spread
rate =  0.01;
delta2 =  0.05;
S20 =  99.0;
sigma2 =  0.3;
ro12 = 0.2;
T =  1.5;


seriex=0:1/N:(1-1/N);
seriey=0:1/N:(1-1/N);
value=0;
for i=seriex
		for j=seriey
	       value=value+hstar(i,j,w1,w2,rate,delta1,delta2,S10,S20,sigma1,sigma2,ro12,T,K);	  
		endfor
endfor
value=value/(N*N)

exp(-rate*T)*margrabe_formula(S10,S20,delta1,delta2,sigma1,sigma2,ro12,T)


