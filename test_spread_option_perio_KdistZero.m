#SPREAD OPTION K<>0
#pesos de la spread option

#parámetros fijos 
K=0;
w1=w2=1;
delta1=delta2=0.05;
rate=0.1;
sigma2=0.2;
S20=100;

numprecios=4;
numsigmas=3;
numperiodos=4;
numro12=3;

S10=1:numprecios;
sigma1=1:numsigmas;
T=1:numperiodos;
ro12=1:numro12;

%Parámetros para la otra pata del spread, el periodo y la correlación
S10=[92,96,100,104];
sigma1=[0.1,0.2,0,3];
T=[1/52,1/12,1,5];
ro12=[-0.5,0,0.5];

m=11;
good_lattice_points; %precisa de definir "m", generando una red de puntos en var "glp"

glpBig=f_glp(26);

models=2;
errorsum=zeros(1,models);

#calculo con metodo numerico: Modelo poly-3
num_param_perio=2;

% |S10|*|sigma1|*|T|*|ro12|=144 posibilidades
for i=1:numprecios
  for j=1:numsigmas
	 for k=1:numperiodos
		for l=1:numro12
		     %calcular el valor de la spread options con los parámetros
		     S10_=S10(i);
			  sigma1_=sigma1(j);
			  ro12_=ro12(l);
			  T_=T(k);

		     mc=spread_option_periodifica(glp,w1,w2,rate,K,S10_,S20,delta1,delta2,sigma1_,sigma2,ro12_,T_,num_param_perio);

			  ref=spread_option(glpBig,w1,w2,rate,K,S10_,S20,delta1,delta2,sigma1_,sigma2,ro12_,T_);

			 
	        errorsum(1,num_param_perio)=errorsum(1,num_param_perio)+f_error(mc,ref);

		endfor
	 endfor
  endfor
endfor


errorfinal=sqrt(errorsum(1,num_param_perio));

%error(1,num_param_perio)=sqrt(error(1,num_param_perio)/144);



%plot(log(vector_N),log(error(:,2)),"-o;Polynomial-3;",
 %    log(vector_N),log(error(:,3)),"-o;Polynomial-4;",     
  %   log(vector_N),log(error(:,6)),"-*;Sin3-Transform;",
   %  log(vector_N),log(error(:,7)),"-x;Sin4-Transform;",
    % log(vector_N),log(error(:,8)),"-x;No Periodization;");


