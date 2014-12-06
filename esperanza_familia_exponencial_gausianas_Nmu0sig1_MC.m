# Calcular la esperanza de una familia de variables aleatorias 
#exponencial de una gausiana de media 0 y variance 1 mediante 
#el método de Monte Carlo. X=exp(beta*G), con G=N(0,1).  
#El resultado teórico de E(exp(be#ta*G))=exp(bete^2/2)

# parametros de la familia
betas=[2,4,6,8,10];
len=length(betas);

# muestras MC
n=100000;

# variable para las muestras
muestras=zeros(n,len);

# variable para las muestras al cuadrado
muestras_cuadrados=zeros(n,len);

# algoritmo
for i=1:n
  G=stdnormal_rnd(1);
  for j=1:len
     X=exp(G*betas(j));
     Y=power(X,2);
     muestras(i,j)=X;
     muestras_cuadrados(i,j)=Y;
  endfor
endfor

# calcular el estimador Monte Carlo para cada caso beta: mean(Xi)
estimadorMC=mean(muestras);

# resultados teoricos
resultadosExactos=exp(power(betas(1),2)/2);
for i=2:len
  resultadosExactos=[resultadosExactos,exp(power(betas(i),2)/2)];
endfor

# calculando los errores
mc=estimadorMC
teo=resultadosExactos
errorAbsoluto=abs(mc-teo)

# Intervalos de confianza: Cantidad de muestras para obtener
# una precision prefijada con una probabilidade del 95%?  
# [media_muestral-1.96*sigma_muestrao/sqrt(n),
# media_muestral+1.96*sigma_muestrao/sqrt(n)]. 
# A partir de los intervalos de confianza, se calculara 
# el valor de n, para que el resulatado se encuentre 
# con un margen de confianza en el rango deseado prefijado.

# calculamos el estimador 
# varianzas empiricas de la muestra: 
# sigma_n= n/(n-1) * (1/n*mean(Yi) - mean(Xi)^2)
estimadorMC2=mean(muestras_cuadrados)

varianzas_muestrales=zeros(len,1);
for i=1:len
   varianzas_muestrales(i)=n/(n-1)*(estimadorMC2(i)-estimadorMC(i)^2);
endfor

varianzas_muestrales(1)/sqrt(n)
varianzas_muestrales(2)/sqrt(n)
varianzas_muestrales(3)/sqrt(n)
varianzas_muestrales(4)/sqrt(n)
varianzas_muestrales(5)/sqrt(n)

