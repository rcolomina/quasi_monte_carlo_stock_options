# INPUT
# N numero de  puntos por variable
# d dimension o numero de variables
# OUTPUT
# array N^d puntos d dimensionales

function f_ret=f_variaciones_repeticion(N,d)
  array=eye(power(N,d)-1,d);
  x=eye(N,1);
  y=1:N;
  for i=0:power(N,d)-1
 
				 base=N;
				 digitos=d;
	 numero=dec2base(i,base,digitos);
    vector=base2dec(numero(1),d)/N;
    for k=2:d

		valor=base2dec(numero(k),N)/N;
		vector=[vector,valor]
    endfor
    array(i+1,:)=vector;
    f_ret=array;
  endfor

endfunction
