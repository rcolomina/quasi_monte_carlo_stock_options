# INPUTS
# N   : numero de punots
# dim : dimension
# OUTPUTS
# Array multidimensional LDS van der corput
function f_return=f_van_der_corput_ndim(N,dim)

  for i=1:N
	 secuenciaN(i)=f_van_der_corput(2,i);
  endfor  

  secuenciaN;

  array=eye(N,dim);

  for j=1:dim
	 permuta=f_permuta_aleatoria(N);
	 for i=1:N
		array(i,j)=secuenciaN(permuta(i));
    endfor
  endfor
 
  f_return=array;

endfunction