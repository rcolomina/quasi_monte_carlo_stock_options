# Iteracion n-esima de un Geometric Brownian Motion
# INPUT : parametros del GBM
# S0 : Precio inicial
# r  : Tipo de interes
# sigma : volatilidad
# delta : dividendo subyacente
# n : iteracion requerida (n<=long(Z))
# T : periodo del GBM
# Z : vector normal gausiano

# Algoritmo de discretizacion: Formula explicita
# S(n) = S0 * exp( r-delta-0.5*sigma2)nT/m+
#            sigma*Raiz(T/m)*suma(Z1+...Zn)

# OUTPUT : Momento n-ésima del GBM definido por vector Z 
function f_return=f_gbm_explicit(S0,r,sigma,delta,n,T,Z)
   m=length(Z);
   if(n>m)
	  printf("Iteracion fuera de rango\n");
   endif
   paso=T/m;
   sumaZ=0;
	if(n==0)
	  f_return=S0;
   else
	  for i=1:n
	    sumaZ=Z(i);
     endfor
     aux1 = exp (( r - delta - 0.5 * sigma * sigma) * n * paso);
     aux2 = exp ( sigma * sqrt(paso) * sumaZ );
	  f_return = S0 * aux1 * aux2;
	endif
endfunction