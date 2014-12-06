# SPREAD OPTIONS
# INPUTS
# u1 en [0,1) :componente x del n-esimo termino de la secuencia de baja discrepancia
# u2 en [0,1) :componente y del n-esimo termino de la secuencia de baja discrepancia
# w1 y w2 : pesos de cada subyacente considerados positivos
# w1 y w2 : pesos de cada subyacente considerados positivos
# rate : tipo de interes
# delta1 y delta2 : dividendos para los subyacente 1 y 2
# S01 y S02 precios de los subyacente en el instante 0
# sigma1 y sigma2 son las volatilidades de los subyacentes
# ro12 en [-1,1] correlación entre los subyacentes
# T tiempo de madurez de las opciones
# K precio del strike del spread
# OUTPUTS
# Devuelve el valor del integrando para calcular la griega gamma1 de una spread option
function f_ret=hstar_gamma1(u1,u2,w1,w2,rate,delta1,delta2,S10,S20,sigma1,sigma2,ro12,T,K)
	 
    #Cambio de variable muiT=log(Si0) + (r-delta(i)-1/2sigma(i)²)*T
	 mu1T = log( S10 ) + ( rate - delta1 - 1/2 * sigma1 * sigma1 ) * T;
    mu2T = log( S20 ) + ( rate - delta2 - 1/2 * sigma2 * sigma2 ) * T;
	 #Descomposicion de matriz de covarianzas en descomposicion de Cholesky: A=C*C'
    c11 = sigma1 * sqrt(T);
    c21 = ro12 * sigma2 * sqrt(T);
    c22 = sqrt( 1 - ro12 * ro12 ) * sigma2 * sqrt(T);

    if(u1>0)
	      h3 = c11 * stdnormal_inv_modif( u1 ) + mu1T;
			h1 = w1 * exp( h3 );        
         g  = ( log ( h1 + K ) - log( w2 ) - mu2T - c21 * stdnormal_inv_modif( u1 ) ) / c22;
         d2 = stdnormal_cdf( g );
         %if((d2+u2*(1-d2))<0.99999999)
 		   h5 = stdnormal_inv_modif( d2 + u2 * ( 1 - d2 ) );
         h4 = c21 * stdnormal_inv_modif( u1 ) + c22 * h5 + mu2T;
         h2 = w2 * exp(h4);
         h  = h2 - h1 - K;
			%calculos intermedios
			a1 = ( h1 / ( ( h1 + K ) * S10 ) );
			a2 = h5 * h5 - g * g;
			%derivadas parciales respecto S1
			dp_h_S1 = ( h1 / S10 ) * ( ( h2 / ( h1 + K ) ) * ( 1 - u2 ) * exp( 0.5 * a2 ) - 1 );
			dp_g_S1 = a1 / c22;  
         dp_d2_S1= ( 1 / sqrt( 2 * pi ) ) * exp( - g * g / 2 ) * dp_g_S1;
			%derivadas parciales segundas respecto S1
			dp_2_h_S1 = h2 * a1 * a1 * ( 1 - u2 ) * exp( 0.5 * a2 ) * ( ( 1 - u2 ) * exp( 0.5 * a2 ) * ( h5 / c22 + 1 ) -g / c22 - 1 );
			dp_2_g_S1 = - a1 * a1 / c22;
			dp_2_d2_S1= dp_d2_S1 * ( ( dp_2_g_S1 / dp_g_S1 ) - dp_g_S1 * g );				  			
			%resultado final para gamma1
         f_ret= ( 1 - d2 ) * dp_2_h_S1 - 2 * dp_h_S1 * dp_d2_S1 - dp_2_d2_S1 * h;
			%else
 			%	 f_ret=0;
         %endif
    else
	     f_ret=0;
    endif

endfunction
