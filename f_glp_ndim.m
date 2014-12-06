# Genera una red de integración usando una Lattile Rule
# de Fibonacci
# Vector de generacion (1,l,l2 mod N,
#INPUTS: 
# m :Numero de puntos de la red de integracion
# d :Dimension de la red
# l :Parámetro libre 1<=l<N
#OUTPUT: 
# Array d-dimensional de m puntos


function f_return=f_glp_ndim(m,dim,l)

  glp=eye(m,dim);
  z=eye(dim,1);
  z=[1,l];
  for i=3:dim
	 z=[z,fmod(power(l,i),m-1)];
  endfor

  for i=1:m
	 for j=1:dim
		x=i*z(j)/m;
		glp(i,j)=fmod(i*z(j)/m,1);
	 endfor
  endfor

  f_return=glp;

endfunction
