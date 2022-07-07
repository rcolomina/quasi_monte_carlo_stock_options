# Función para transformar un número natural en 
# su correspondintente de la secuencia de Van der Corput
#
# INPUT 
# b : base
# n : numero
# OUTPUT
# c : numero n transformado en la secuencia 
function f_return=f_van_der_corput(b,n)

n0=n;
c=0;
ib=1/b;
while(n0>0)
  n1=floor(n0/b);
  i=n0-n1*b;
  c=c+ib*i;
  ib=ib/b;
  n0=n1;
endwhile

f_return=c;

endfunction