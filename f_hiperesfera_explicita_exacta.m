# INPUTS
# x vector del dominio

function f_ret=f_hiperesfera_explicita_exacta(x,R)

  sum=0;
  for i=1:length(x)
	 sum+=x(i)*x(i);
  endfor

  if(sum<=R*R)
	 f_ret=sqrt(R*R-sum);
  else
	 f_ret=0;
  endif


endfunction
