%Generacion de N movientos brownianos geometricos

% condiciones iniciales para el GBM
T=2;
n=1000;
rate=0.1;
delta=0.01;
sigma=0.4;
S0=10;

% generamos N=10 GBM
N=100;

var=eye(N,2);
for i=1:N
  bm=f_geometric_brownian_motion(T,n,rate,delta,sigma,S0);

  var(i,1)=bm(N/2);
  var(i,2)=bm(N);

  hold on
  plot(bm,'r');
endfor

corr(var(:,1),var(:,2))
