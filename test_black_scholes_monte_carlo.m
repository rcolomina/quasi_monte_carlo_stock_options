#Simulacion MC del modelo de Black Scholes 

# INPUTS 
# S0    : precio inicial 
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo 

S0=100; 
K=90; 
rate=0.01; 
delta=0.05; 
sigma=0.3; 
T=1; 

#Variable aleatoria ST LOG-NORMAL 
# ST = S0*exp{(rate-delta-sigma*sigma)/2)*T+sigma*sqrt(T)*G}

#En el modelo de Black-Scholes, el precio de la opcion es
# p = E [exp(-rate * T) * max(ST-K,0)]

valor=0;
error_estandart=0;

numsigmas=4; #numero sigmas probados
sigma=0;

itera=15; #numero de estimaciones
vector_estimador=zeros(itera,numsigmas);
for sig=1:numsigmas
  sigma=sigma+0.1;
  alfa=((rate-delta-sigma*sigma)/2)*T;
  beta=sigma*sqrt(T);
  for j=1:itera
    #Simular muestras de var. i.i.d gausianas 
    vector_gaussiano;
    for i=1:n
      ST=S0*exp(alfa+beta*vgauss(i));
      valor=valor+max(ST-K,0);
    endfor
    valor=exp(-rate*T)*valor/n;
    #Almacenar la estimacion optenida en cada iteracion
    vector_estimador(j,sig)=valor;
  endfor
endfor

errores_standard=1:numsigmas;
for sig=1:numsigmas
    errores_standard(sig)=error_standard(vector_estimador(:,sig));
endfor



