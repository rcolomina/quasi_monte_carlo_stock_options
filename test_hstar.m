N=10;
w1=w2=1;
K=0;
S10=100;
sigma1=0.3;
delta1=0.05;

S20=unifrnd(50,130); #S20
sigma2=unifrnd(0.1,0.5); #sigma2
delta2=unifrnd(0.01,0.1); #delta2

#valores de entorno y relacion entre subyacentes
T=unifrnd(0.5,1); #T
rate=unifrnd(0.01,0.15); #r
ro12=unifrnd(-0.8,0.8); #ro12


seriex=0:1/N:(1-1/N);
seriey=0:1/N:(1-1/N);
value=0;
for i=seriex
		for j=seriey
	       value=value+hstar(i,j,w1,w2,rate,delta1,delta2,S10,S20,sigma1,sigma2,ro12,T,K);	  
		endfor
endfor
value=value/(N*N);


