# Generador de secuencias de Van der Corput
# INPUT 
# b : base
# N : tamaño de la secuencia
# OUTPUT
# Secuencia de Vander Corput en [0,1]x[0,1]
# Secuencia uniforme bidimensional en [0,1]x[0,1]

baseX=2;
baseY=3;

N=100;

vdc=eye(N,2);
vur=eye(N,2);
%Secuencia bidimensional
for i=1:N
  x=f_van_der_corput(baseX,i);
  y=f_van_der_corput(baseY,i);
  vdc(i,1)=x;
  vdc(i,2)=y;
  vur(i,1)=rand;
  vur(i,2)=rand;
 
endfor
plot(vdc(:,1),vdc(:,2),'o')
#plot(vRand(:,1),vRand(:,2),'*',v(:,1),v(:,2),'o')
