# SPREAD OPTIONS
# u1 en [0,1) :componente x del n-esimo termino de la serie de baja discrepancia
# u2 en [0,1) :componente y ...
# w1 y w2 : pesos de cada subyacente considerados positivos
# rate : tipo de interes
# delta1 y delta2 : dividendo subyacente 1 y 2
# S01 y S02 precios de los subyacente en el instante 0
# sigma1 y sigma2 son las volatilidades de los subyacentes
# ro12 en [-1,1]
# T tiempo de madurez de las opciones
# K precio del strike del spread
# Subyacente para calcular su gamma de la spread opción: valores posibles 1 o 2
function f_ret=hstar_gamma(u1,u2,w1,w2,rate,delta1,delta2,S10,S20,sigma1,sigma2,ro12,T,K,subyacente)
	 
    #Cambio de variable muiT=log(Si0) + (r-delta(i)-1/2sigma(i)²)*T
	 mu1T=log(S10)+(rate-delta1-1/2*sigma1*sigma1)*T;
    mu2T=log(S20)+(rate-delta2-1/2*sigma2*sigma2)*T;
	 #Descomposicion de matriz de covarianzas en descomposicion de Cholesky: A=C*C'
    c11=sigma1*sqrt(T);
    c21=ro12*sigma2*sqrt(T);
    c22=sqrt(1-ro12*ro12)*sigma2*sqrt(T);

#    alpha=1.0e-08;
 #   beta=1.0-1.0e-10;

    if(u1>0)
	      h3=c11*stdnormal_inv_modif(u1)+mu1T;
			h1=w1*exp(h3);        
         g=(log(h1+K)-log(w2)-mu2T-c21*stdnormal_inv_modif(u1))/c22;
         d2=stdnormal_cdf(g);
         if((d2+u2*(1-d2)))#<0.9999999999) 
				  h5=stdnormal_inv_modif(d2+u2*(1-d2));
              h4=c21*stdnormal_inv_modif(u1)+c22*h5+mu2T;
              h2=w2*exp(h4);
              h=h2-h1-K;

				  Saux=1;
				  parcial_h_Si=0;
				  if(subyacende==1)
					 Saux=S1;
				  else 
				    Saux=S2;
				 
				  %derivadas parciales respecto Si
				  parcial_h_Si=(h1/Saux)*(h2/(h1+K)*(1-u2)*exp(0.5*(h5*h5-g*g)));			          	partial_d2_Si=(1/sqrt(2*pi))*exp(-g*g/2)*h1/(c22*(h1+K)*Saux);
	 
              f_ret=(1-d2)*parcial_h_Si-parcial_d2_Si*h;
			else
 				 f_ret=0;
         endif
    else
	     f_ret=0;
    endif

endfunction
