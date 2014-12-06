# Test estimador opcion call europea usando likelihood ratio

# INPUTS 
# S0    : precio subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo

#Condiciones iniciales de la simulacion
S0 = 110;
K = 100;
rate = 0.1;
delta = 0.03;
sigma = 0.25;
T = 0.2;

# Tamaño muestral
N=10000;

% Generars N muestras aleatorias de Z distribución normal estandar
Z=stdnormal_rnd(N,1); 
%DELTAwithControl=eye(N,1);

% Calcular ST lognormal var. aleatoria desde Z
ST=lognormal_random_ST(S0,rate,delta,sigma,T,Z);

# ESTIMACION DELTA
DELTA=eye(N,1);
AUXPLOT1=eye(N,1);

for i=1:N	 
	 DELTA(i)=european_call_estimador_likelihood_delta(S0,ST(i),K,rate,delta,sigma,T);
    AUXPLOT1(i)=mean(DELTA(1:i));
endfor

EstimacionLikelihoodDelta=mean(DELTA);
StandardErrorMeanEstimacionDelta=standard_error(DELTA);

EstimacionLikelihoodDelta
StandardErrorMeanEstimacionDelta

# ESTIMACION VEGA
VEGA=eye(N,1);
AUXPLOT2=eye(N,1);

for i=1:N	 
	 VEGA(i)=european_call_estimador_likelihood_vega(S0,ST(i),K,rate,delta,sigma,T);
    AUXPLOT2(i)=mean(VEGA(1:i));
endfor

EstimacionLikelihoodVega=mean(VEGA);
StandardErrorMeanEstimacionVega=standard_error(VEGA);

EstimacionLikelihoodVega
StandardErrorMeanEstimacionVega

# ESTIMACION GAMMA
GAMMA=eye(N,1);
AUXPLOT1=eye(N,1);

for i=1:N	 
	 GAMMA(i)=european_call_estimador_likelihood_gamma(S0,ST(i),K,rate,delta,sigma,T);
    AUXPLOT1(i)=mean(GAMMA(1:i));
endfor

EstimacionLikelihoodGamma=mean(GAMMA);
StandardErrorMeanEstimacionGamma=standard_error(GAMMA);

EstimacionLikelihoodGamma
StandardErrorMeanEstimacionGamma

# ESTIMACION RHO
RHO=eye(N,1);
AUXPLOT1=eye(N,1);

for i=1:N	 
	 RHO(i)=european_call_estimador_likelihood_rho(S0,ST(i),K,rate,delta,sigma,T);
    AUXPLOT1(i)=mean(RHO(1:i));
endfor

EstimacionLikelihoodRho=mean(RHO);
StandardErrorMeanEstimacionRho=standard_error(RHO);

EstimacionLikelihoodRho
StandardErrorMeanEstimacionRho

# ESTIMACION THETA
THETA=eye(N,1);
AUXPLOT1=eye(N,1);

for i=1:N	 
	 THETA(i)=european_call_estimador_likelihood_theta(S0,ST(i),K,rate,delta,sigma,T);
    AUXPLOT1(i)=mean(THETA(1:i));
endfor

EstimacionLikelihoodTheta=mean(THETA);
StandardErrorMeanEstimacionTheta=standard_error(THETA);

EstimacionLikelihoodTheta
StandardErrorMeanEstimacionTheta