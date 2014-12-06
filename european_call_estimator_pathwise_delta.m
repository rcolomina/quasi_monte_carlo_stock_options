# Estimador pathwise de una opcion Call Europea
# INPUTS 
# S0    : precio subyacente
# ST    : precio final en T
# K     : strike price 
# rate  : tipo interes
# T     : periodo 
# OUTPUT
# Delta d(precio)/dS0
function f_return=european_call_estimator_pathwise_delta(S0,ST,K,rate,T)

  if( ST >= K )
    f_return = exp(-rate*T) * ST / S0;
  else
	 f_return = ST * 0;
  endif


endfunction
