# Test del estimador pathwise con control de varianza para una opcion call Asiática 

#INPUTS 
# S0    : precio subyacente
# K     : strike price 
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo en años
# m     : ultimos días a precio de cierre
# n     : numero paso discretizacion GBM
# h     : paso de la resimulacion
# a     : año en dias
# N     : numero de GBM generados

#OUTPUT
# Precio opción call asiática
# Precio opción call asiática con Resimulación
# Delta Pathwise 
# Delta con Resimulacon

# Vega  : d(precio)/d(sigma)
# Gamma : d2(p)/d2(S0)
# Rho   : d(precio)/d(rate)
# Theta : -d(precio)/d(T)

% Condiciones iniciales de la simulacion
%S0=[90,100,110];
S0=90;
K=100;
rate=0.1;
delta=0.03;
sigma=0.25;
T=0.2;
m=30;
n=150;
h=0.0001;
a=365.25;
N=10000; 

%Reserva de memoria
ST=eye(N,1);
Z=eye(N,1)

ASIAN=eye(N,1); 
ASIANwithControl=eye(N,1); 

DELTA=eye(N,1);
DELTAwithControl=eye(N,1);

ST=eye(1,m);
STresimula=eye(1,m);

ASIAN=eye(N,1);
ASIANpertur=eye(N,1);

DeltaResimula=eye(N,1);
DeltaResimulaControl=eye(N,1);


%VEGA=eye(N,1);
%VEGAwithControl=eye(N,1);
%RHO=eye(N,1);
%RHOwithControl=eye(N,1);
%THETA=eye(N,1);
%THETAwithControl=eye(N,1);

% Muestras de la distribución normal estandar Z
%Z=stdnormal_rnd(N,1);
% Vector ST lognormal desde Z
%ST=lognormal_random_ST(S0,rate,delta,sigma,T,Z);

% Generación de N de caminos GBM: N filas y m columnas
MatrizGBM  = eye(N,n);          %matriz N GBMs n iteraciones
MatrizGBMresimula = eye(N,n);   %matriz N GBMs n iteraciones
MatrizGBM2 = eye(N,m);          %matriz N GBMs m ultimos dias precios a cierre
MatrizGBM2resimula = eye(N,m);  %matriz N GBMs n iteraciones


%%%%%%%GENERACION DE N GBM%%%%%%
t0=clock();
for i=1:N
   Z=stdnormal_rnd(n,1);
   MatrizGBM(i,:)=f_geometric_brownian_motion_2(T,Z,rate,delta,sigma,S0);
   MatrizGBMresimula(i,:)=f_geometric_brownian_motion_2(T,Z,rate,delta,sigma,S0+h);
endfor
elapse_time_t0=etime(clock(),t0)

%%%%%EXTRAER LOS ULTIMOS M DIAS%%%%
t1=clock();
for i=1:N
 % Para cada GBM nos quedamos con los últimos m dias
  for j=1:m
   %convertir indice de GBM a dias
    d=floor(n*(T*a-j+1)/(T*a));
    MatrizGBM2(i,m-j+1)=MatrizGBM(i,d);
    MatrizGBM2resimula(i,m-j+1)=MatrizGBMresimula(i,d);
  endfor
endfor
elapse_time_t1=etime(clock(),t1)

%d=floor(n*(T*a-m)/(T*a));
%S0GMB2=MatrizGBM(:,d);



STresimula=MatrizGBM2resimula(:,30);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%PRECIO OPCION CALL ASIATICA CON MEDIA ARITMETICA%%%%

for i=1:N
  GBM=MatrizGBM2(i,:);
  ASIAN(i)=asian_call_estimator_aritmetic_average_price(S0,GBM,K,rate,T);
endfor
EstASIANPriceCallAsian=mean(ASIAN)
stderrPriceCallAsian=standard_error(ASIAN)
printf("-----\n");

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%PRECIO OPCION CALL ASIATICA CON MEDIA ARITMETICA CON CONTROL%%%%



ST=MatrizGBM2(:,30);
beta = - cov(ASIAN,ST)/var(ST)
for i=1:N
    ASIANwithControl(i) = ASIAN(i) + beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
	 %AUXPLOT2(i)=mean(DELTAwithControl(1:i));
endfor
EstASIANPriceWithControl=mean(ASIANwithControl)
stderrEstASIANPriceWithControl=standard_error(ASIANwithControl)
printf("-----\n");

%%%%%%%%%%%%%%%%%%%%%
%%%DELTA PATHWISE%%%%
%AUXPLOT1=eye(N,1);
%AUXPLOT2=eye(N,1);
for i=1:N
    GBM=MatrizGBM2(i,:);
	 DELTA(i)=asian_call_estimator_pathwise_delta(S0,GBM,K,rate,T);
%    AUXPLOT1(i)=mean(DELTA(1:i));
endfor
EstDeltaPW = mean(DELTA)
stderrMeanEstDeltaPW = standard_error(DELTA)
printf("-----\n");

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%DELTA PW WITH CONTROL%%%

% calculamos beta para el estimador
beta = - cov(DELTA,ST)/var(ST)

for i=1:N
    DELTAwithControl(i) = DELTA(i) + beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
%	 AUXPLOT2(i)=mean(DELTAwithControl(1:i));
endfor
EstDeltaPWwithControl=mean(DELTAwithControl)
stderrMeanEstDeltaPWwithControl=standard_error(DELTAwithControl)
printf("-----\n");



%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%DELTA CON RESIMULACION%%%


for i=1:N
  GBM=MatrizGBM2(i,:);
  GBMpertur=MatrizGBM2resimula(i,:);
  ASIAN(i)=asian_call_estimator_aritmetic_average_price(S0,GBM,K,rate,T);
  ASIANpertur(i)=asian_call_estimator_aritmetic_average_price(S0,GBMpertur,K,rate,T);
  DeltaResimula(i)=(ASIANpertur(i)-ASIAN(i))/h;

endfor

EstDeltaWithRersimula=mean(DeltaResimula)
stderrDeltaWithResimula=standard_error(DeltaResimula)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%DELTA CON RESIMULACION CON CONTROL%%%
beta = - cov(DeltaResimula,ST)/var(ST)
for i=1:N
  DeltaResimulaControl(i)=DeltaResimula(i)+beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
endfor

EstDeltaWithRersimulaControl=mean(DeltaResimulaControl)
stderrDeltaWithResimulaControl=standard_error(DeltaResimulaControl)



%EstDeltaWithError=mean(DELTAWITHERROR)

%%%VEGA%%%
%for i=1:N
%    GBM=MatrizGBM2(i,:);
%	 VEGA(i)=asian_call_estimator_pathwise_vega(S0,GBM,K,rate,delta,sigma,T);
%endfor

%EstVega=mean(VEGA)
%stderrMeanEstVega=standard_error(VEGA)


%for i=1:N
 %   GBM=MatrizGBM2(i,:);
%	 VEGA(i)=asian_call_estimator_likelihood_vega(S0,GBM,K,rate,delta,sigma,T);
%endfor

%EstVegaLR=mean(VEGA)
%stderrMeanEstVegaLR=standard_error(VEGA)


%for i=1:N
%    GBM=MatrizGBM2(i,:);
%	 GAMMA(i)=asian_call_estimator_likelihood_gamma(S0,GBM,K,rate,delta,sigma,T);
%endfor

%EstGammaLR=mean(GAMMA)
%stderrMeanEstGammaLR=standard_error(GAMMA)




%beta = - cov(VEGA,ST)/var(ST)
%for i=1:N
%    VEGAwithControl(i)=VEGA(i)+ beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
%endfor
%EstVegaWithControl=mean(VEGAwithControl)
%stderrMeanEstVegaWithControl=standard_error(VEGAwithControl)

%%%RHO%%%
%for i=1:N
%	 RHO(i)=asian_call_estimador_pathwise_rho(S0,ST(i),K,rate,delta,sigma,T);
%endfor
%beta = - cov(RHO,ST)/var(ST)
%EstRho=mean(RHO)
%stderrMeanEstRho=standard_error(RHO)
%for i=1:N
%    RHOwithControl(i)=RHO(i)+ beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
%endfor
%EstRhoWithControl=mean(RHOwithControl)
%stderrMeanEstRhoWithControl=standard_error(RHOwithControl)

%%%THETA%%%
%for i=1:N
%	 THETA(i)=asian_call_estimador_pathwise_theta(S0,ST(i),K,rate,delta,sigma,T);
%endfor
%beta = - cov(THETA,ST)/var(ST)
%EstTheta=mean(THETA)
%stderrMeanEstTheta=standard_error(THETA)
%for i=1:N
%    THETAwithControl(i)=THETA(i)+ beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
%endfor
%EstThetaWithControl=mean(THETAwithControl)
%stderrMeanEstThetaWithControl=standard_error(THETAwithControl)



