
% INPUT:
% n dimension
% r radio
% OUTPUT: Volumen

function f_ret=f_hiperesfera_volumen_cuadratura(n,r)

%precision por variable
m=10;

%creamos una variable por cada dimension
grid=eye(n,m);
for i=1:n
  for k=1:m
    grid(i,k)=k/m;
  endfor
endfor
  
%crear todas las combinaciones posibles de elementos con el grid












%aplicamos el grid a la funcion test