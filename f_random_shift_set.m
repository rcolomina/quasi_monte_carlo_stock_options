# INPUT
# Array bidimensional en [0,1)^2
# OUTPUT
# Array bidimensional desplazado aleatoriamente en [0,1)^2
function f_retorno=f_random_shift_set(glp)

  #crer un vector aleatorio aleatorios en [0,1)^2
  N=length(glp);
  angle=rand;
  vector_rand=[cos(angle),sin(angle)];
  vector_rand/=norm(vector_rand);

  #desplazar el conjunto
  shifted_glp=eye(length(glp),2);
  shifted_glp(:,1)=glp(:,1)+vector_rand(1);
  shifted_glp(:,2)=glp(:,2)+vector_rand(2);

  #volver al espacio de partida
  shifted_glp(:,1)=fmod(shifted_glp(:,1),1);
  shifted_glp(:,2)=fmod(shifted_glp(:,2),1);

  f_retorno=shifted_glp;
endfunction
