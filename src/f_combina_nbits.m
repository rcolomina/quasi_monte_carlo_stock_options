#imprimer combinaciones posibles vector n bits

function f_ret=f_combina_nbits(n)
  y=eye(n,1);
  if(n==1)
     for x=0:1
		  y(1)=x;
        f_ret=y
     endfor
  else
     for bit=0:1
        y(n)=bit;
  		  f_ret=y
        f_combina_nbits(n-1);
	  endfor
   endif
endfunction