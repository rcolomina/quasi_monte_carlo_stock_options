% Estimador de Vega para una opcion call europea usando pathwise
% INPUTS 
% S0    : precio subyacente
% ST    : precio final en T
% K     : strike price 
% rate  : tipo interes
% delta : dividendo
% sigma : volatilidad
% T     : periodo 
% OUTPUT
% Vega d(precio)/d(sigma) (ST): Depende de la muestra
function f_return=european_call_estimator_pathwise_vega(S0,ST,K,rate,delta,sigma,T)

  sigma2=sigma*sigma;

  aux = ( ST / sigma) * ( log ( ST / S0 ) - ( rate - delta + 0.5 * sigma2 ) * T );

  if( ST >= K )
    f_return = exp( - rate * T ) * aux;
  else
	 f_return = 0;
  endif

endfunction
