#INPUTS 
# S0    : precio subyacente
# rate  : tipo interes
# delta : dividendo
# sigma : volatilidad
# T     : periodo en años
# N     : numero de GBM
# n     : numero de pasos de discretizacion para cada GBM
    

#OUTPUT
# Matriz Nxn con N GBM de n iteraicones

function f_return=f_generador_matriz_gbm(S0,rate,delta,sigma,T,n,N)

  MatrizGBM  = eye(N,n);  %matriz N GBMs n iteraciones

  for i=1:N
      MatrizGBM(i,:)=f_geometric_brownian_motion(T,n,rate,delta,sigma,S0);
  endfor

  f_return=MatrizGBM
  
endfunction