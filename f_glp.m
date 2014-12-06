# Genera una red de integración usando una Lattile Rule
# de Fibonacci
#INPUTS: 
# m :Numero de puntos de la red de integracion
#OUTPUT: 
# Array bidimensional de tamaño m

function f_return=f_glp(m)

  fibo=1:m;
  fibo(1)=1;fibo(2)=1;
  for i=3:m
	   fibo(i)=fibo(i-1)+fibo(i-2);
	endfor
   %generamos la sucesion good laticce points 
   N=fibo(m);
   glp=eye(N,2);

   z=[1,fibo(m-1)];

   for i=1:N
	  glp(i,1)=fmod(i*z(1)/N,1);
	  glp(i,2)=fmod(i*z(2)/N,1);
   endfor

   f_return=glp;

endfunction