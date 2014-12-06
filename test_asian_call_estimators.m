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
# Delta Pathwise con Control 
# Delta Resimulacon
# Delta Resimulacion con Contro

% Condiciones iniciales de la simulacion
%S0=[90,100,110];
S0=110
K=100;
rate=0.1;
delta=0.03;
sigma=0.25;
T=0.2;
m=30;
n=200;
h=0.0001;
a=365.25;
N=10000; 

% Reserva de memoria
ST=eye(N,1);
Z=eye(N,1);

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

% Generación de N de caminos GBM: N filas y m columnas
MatrizGBM  = eye(N,n);          %matriz N GBMs n iteraciones
MatrizGBMresimula = eye(N,n);   %matriz N GBMs n iteraciones
MatrizGBM2 = eye(N,m);          %matriz N GBMs m ultimos dias precios a cierre
MatrizGBM2resimula = eye(N,m);  %matriz N GBMs m ultimos dias precios a cierre

%%%%%%%GENERACION DE N GBM%%%%%%
t0=clock();
for i=1:N
   Z=stdnormal_rnd(n,1);
   MatrizGBM(i,:)=f_geometric_brownian_motion_2(T,Z,rate,delta,sigma,S0);
   MatrizGBMresimula(i,:)=f_geometric_brownian_motion_2(T,Z,rate,delta,sigma,S0+h);
endfor
elapse_time_t0=etime(clock(),t0)

%%%%%EXTRAER LOS ULTIMOS M DIAS DEL GBM%%%%
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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%PRECIO OPCION CALL ASIATICA CON MEDIA ARITMETICA%%%%
t0=clock();
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
beta = - cov(ASIAN,ST)/var(ST);
for i=1:N
    ASIANwithControl(i) = ASIAN(i) + beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
	 %AUXPLOT2(i)=mean(DELTAwithControl(1:i));
endfor
EstASIANPriceWithControl=mean(ASIANwithControl)
stderrEstASIANPriceWithControl=standard_error(ASIANwithControl)
printf("-----\n");

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%DELTA PATHWISE MC CRUDO%%%%
for i=1:N
    GBM=MatrizGBM2(i,:);
	 DELTA(i)=asian_call_estimator_pathwise_delta(S0,GBM,K,rate,T);
endfor
EstDeltaPW = mean(DELTA)
stderrMeanEstDeltaPW = standard_error(DELTA)
printf("-----\n");

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%DELTA PW WITH CONTROL%%%
% calculamos beta para el estimador
beta = - cov(DELTA,ST)/var(ST);
for i=1:N
    DELTAwithControl(i) = DELTA(i) + beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
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
printf("-----\n");

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%DELTA CON RESIMULACION Y CONTROL%%%
STresimula=MatrizGBM2resimula(:,30);
beta = - cov(DeltaResimula,STresimula)/var(STresimula);
for i=1:N
  DeltaResimulaControl(i)=DeltaResimula(i) + beta * ( ST(i) - exp ( ( rate - delta ) * T ) * S0 );
endfor

EstDeltaWithRersimulaControl=mean(DeltaResimulaControl)
stderrDeltaWithResimulaControl=standard_error(DeltaResimulaControl)
printf("-----\n");

elapse_time_t1=etime(clock(),t0)






