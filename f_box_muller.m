# INPUT : Media y Varianza
# Media : mu
# Varianza : sigma
# OUTPUT: Valor aleatorio distribución normal de
# media mu y varianza sigma
function f_return=f_box_muller(mu,sigma)
  U1 = rand();
  U2 = rand();

  Z = sqrt( -2 * log(U1) ) * cos ( 2 * pi * U2 );

  f_return = sigma * Z + mu;
endfunction