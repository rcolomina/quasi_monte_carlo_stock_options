# Test del estimador de una opcion call europea usando likelihood con control de varianza

#INPUTS 
# S0    : precio subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo

#OUTPUT
# Delta d(precio)/dS0

% Condiciones iniciales de la simulacion
S0=90;
K=100;
rate=0.1;
delta=0.03;
sigma=0.25;
T=0.2;
% Tamaño de la muestra aleatoria
N=10000;

% Generamos N muestras aleatorias de Z distribución normal estandar
Z=stdnormal_rnd(N,1);
DELTA=eye(N,1);
DELTAwithControl=eye(N,1);

%ST=eye(N,1);
% Aplicamos las muestras al estimador likelihood de delta
% S0 = 90,100,110
%S0=[90,100,110];

%for k=1:length(S0)
  % Calculamos ST lognormal variable aleatoria desde Z
ST=lognormal_random_ST(S0,rate,delta,sigma,T,Z);

AUXPLOT1=eye(N,1);

for i=1:N
	 DELTA(i)=european_call_estimador_likelihood_delta(S0,ST(i),K,rate,delta,sigma,T);
    AUXPLOT1(i)=mean(DELTA(1:i));
endfor

EstDelta=mean(DELTA)
stderrMeanEstDelta=standard_error(DELTA)

% calculamos beta para el estimador
beta = - cov(DELTA,ST)/var(ST)

%mean(ST)
%exp ( ( rate - delta )* T ) * S0

AUXPLOT2=eye(N,1);

for i=1:N
    DELTAwithControl(i)=DELTA(i)+ beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
	 AUXPLOT2(i)=mean(DELTAwithControl(1:i));
endfor

EstDeltaWithControl=mean(DELTAwithControl)
stderrMeanEstDeltaWithControl=standard_error(DELTAwithControl)
%EstDeltaWithError=mean(DELTAWITHERROR)



