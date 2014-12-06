# Test del estimador pathwise con control de varianza para una opcion call Europea 

#INPUTS 
# S0    : precio subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo

#OUTPUT
# Delta : d(precio)/d(S0)
# Vega  : d(precio)/d(sigma)
# Rho   : d(precio)/d(rate)
# Theta : -d(precio)/d(T)

% Condiciones iniciales de la simulacion
%S0=[90,100,110];
S0=110;
K=100;
rate=0.1;
delta=0.03;
sigma=0.25;
T=0.2;

% Tamaño de la muestra aleatoria
N=10000;

%Reserva de memoria
ST=eye(N,1);
DELTA=eye(N,1);
DELTAwithControl=eye(N,1);
VEGA=eye(N,1);
VEGAwithControl=eye(N,1);
RHO=eye(N,1);
RHOwithControl=eye(N,1);
THETA=eye(N,1);
THETAwithControl=eye(N,1);

% Generación de N muestras aleatorias para una distribución normal estandar Z
Z=stdnormal_rnd(N,1);

% Vector ST lognormal desde Z
ST=lognormal_random_ST(S0,rate,delta,sigma,T,Z);

%%%DELTA%%%
AUXPLOT1=eye(N,1);
AUXPLOT2=eye(N,1);
for i=1:N
	 DELTA(i)=european_call_estimador_pathwise_delta(S0,ST(i),K,rate,T);
    AUXPLOT1(i)=mean(DELTA(1:i));
endfor
EstDelta=mean(DELTA)
stderrMeanEstDelta=standard_error(DELTA)
% calculamos beta para el estimador
beta = - cov(DELTA,ST)/var(ST)
for i=1:N
    DELTAwithControl(i)=DELTA(i)+ beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
	 AUXPLOT2(i)=mean(DELTAwithControl(1:i));
endfor
EstDeltaWithControl=mean(DELTAwithControl)
stderrMeanEstDeltaWithControl=standard_error(DELTAwithControl)
%EstDeltaWithError=mean(DELTAWITHERROR)


%%%VEGA%%%
for i=1:N
	 VEGA(i)=european_call_estimador_pathwise_vega(S0,ST(i),K,rate,delta,sigma,T);
endfor
beta = - cov(VEGA,ST)/var(ST)
EstVega=mean(VEGA)
stderrMeanEstVega=standard_error(VEGA)
for i=1:N
    VEGAwithControl(i)=VEGA(i)+ beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
endfor
EstVegaWithControl=mean(VEGAwithControl)
stderrMeanEstVegaWithControl=standard_error(VEGAwithControl)

%%%RHO%%%
for i=1:N
	 RHO(i)=european_call_estimador_pathwise_rho(S0,ST(i),K,rate,delta,sigma,T);
endfor
beta = - cov(RHO,ST)/var(ST)
EstRho=mean(RHO)
stderrMeanEstRho=standard_error(RHO)
for i=1:N
    RHOwithControl(i)=RHO(i)+ beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
endfor
EstRhoWithControl=mean(RHOwithControl)
stderrMeanEstRhoWithControl=standard_error(RHOwithControl)

%%%THETA%%%
for i=1:N
	 THETA(i)=european_call_estimador_pathwise_theta(S0,ST(i),K,rate,delta,sigma,T);
endfor
beta = - cov(THETA,ST)/var(ST)
EstTheta=mean(THETA)
stderrMeanEstTheta=standard_error(THETA)
for i=1:N
    THETAwithControl(i)=THETA(i)+ beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
endfor
EstThetaWithControl=mean(THETAwithControl)
stderrMeanEstThetaWithControl=standard_error(THETAwithControl)



