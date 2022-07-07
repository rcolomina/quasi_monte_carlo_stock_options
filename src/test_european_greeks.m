% EUROPEAN OPTIONS: GREEKS
%Condiciones iniciales 
S0=90;
K=100;
rate=0.1;
delta=0.03;
sigma=0.25;
T=0.2;

precios=[90,100,110];


for i=1:length(precios)
   printf("Precio: %f \n",precios(i));
   european_call_delta(precios(i),K,rate,delta,sigma,T)
	european_call_vega(precios(i),K,rate,delta,sigma,T)
	european_call_gamma(precios(i),K,rate,delta,sigma,T)
	european_call_rho(precios(i),K,rate,delta,sigma,T)
	european_call_theta(precios(i),K,rate,delta,sigma,T)
endfor