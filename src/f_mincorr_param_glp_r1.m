#INPUT
# N : numero de puntos
# dim : dimension
# Complejidad del orden N^2*dim
#OUTPUT
# Red con correlacion minima entre pares 
function f_return=f_mincorr_param_glp_r1(N,dim)

  parametro=0;
  correlacion_antigua=0.2;
 

  for k=2:N-1
	 tam=dim*(dim-1)/2;
	 correlacion=zeros(tam,1);

    index=0;
    punto_lattice=f_glp_ndim(N,dim,k);
	 for i=1:(dim-1)
		for j=(i+1):dim
		  index=index+1;
		  correlacion(index)=corr(punto_lattice(:,i),punto_lattice(:,j));
		endfor
		correlacion_nueva=max(abs(correlacion));
	 endfor

	 if(correlacion_nueva<correlacion_antigua)
		parametro=k;
      correlacion_antigua=correlacion_nueva;
    endif


  endfor

  f_return=parametro;

endfunction