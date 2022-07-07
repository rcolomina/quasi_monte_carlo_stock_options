# INPUTS
# n : orden de la permutacion
# OUTPUT
# vector de tam. n con permutacion aleatoria
function f_return=f_permuta_aleatoria(n)

  x=1;
  for i=2:n
	 x=[x,i];
  endfor

  for i=1:n-1
	 aleat=floor(rand*(n-i+1))+1;
	 y(i)=x(aleat);
	 if(aleat==1)
		x=x(2:n-i+1);
    else if(aleat==n-i+1)
		x=x(1:n-i);
    else
  	   x=[x(1:aleat-1),x(aleat+1:n-i+1)];
    endif   
    endif

  endfor
  y(n)=x;

  f_return=y;

endfunction