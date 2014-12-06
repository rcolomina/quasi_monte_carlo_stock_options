#generamos la sucesion de fibonacci de N terminos. Definir variable m global antes de ejecutar este script
fibo=1:m;
fibo(1)=1;fibo(2)=1;
for i=3:m
	  fibo(i)=fibo(i-1)+fibo(i-2);
endfor
#generamos la sucesion good laticce points 
N=fibo(m);
glp=eye(N,2);

z=[1,fibo(m-1)];

for i=1:N
	  glp(i,1)=fmod(i*z(1)/N,1);
	  glp(i,2)=fmod(i*z(2)/N,1);
endfor

%plot(glp(:,1),glp(:,2),"x");
