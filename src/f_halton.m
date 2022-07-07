# Generador de secuencias de Halton
# INPUT 
# v : Vector de coprimos
# N : tamaño de la secuencia
# OUTPUT
# Secuencia de Halton de N en [0,1]^s

function f_return=f_halton(v,N)

u=eye(N,length(v));
for i=1:N
  for j=1:length(v)
	 u(i,j)=f_van_der_corput(v(j),i);
  endfor
endfor

f_return=u;

endfunction

