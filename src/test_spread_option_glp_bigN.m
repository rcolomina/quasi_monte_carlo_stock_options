
%test para calcular una spread option usando una red glp de N grande.

%Comentar/descomentar las siguientes línesa para generar la glp
%m=26;
%good_lattice_points;

%condiciones iniciales
w1=w2=1;
K=0;

%condiciones para la primera pata
S10=100;
S20=100;
delta1=0.05;
sigma1=0.3;

%aleatorización para la segunda pata
T=unifrnd(0.5,1);
sigma2=unifrnd(0.1,0.5);
delta2=unifrnd(0.01,0.1);
ro12=unifrnd(-0.8,0.8);
rate=unifrnd(0.01,0.15);

errorsum=0;

mc=spread_option(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);
mf=margrabe_formula(S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);

errorsum=sqrt(f_error(mc,mf));
