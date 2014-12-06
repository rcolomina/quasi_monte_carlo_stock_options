# Estimador de una opcion Call Asiática 
# INPUTS 
# S0    : precio subyacente
# S     : vector de precios 
# K     : strike price 
# rate  : tipo de interés
# T     : momento de maduración
# OUTPUT
# Asian Call aritmetic average price
# Precio = E(exp^(-rT)*max(Promedio(S)-K,0)]

function f_return=asian_call_estimator_aritmetic_average_price(S0,S,K,rate,T)

  aux1 = exp ( - rate * T );

  aux2 = max( mean ( S ) - K , 0 );

  f_return = aux1 * aux2;

endfunction