%Funcion para generar una muestra aleatoria lognormal multivariante


# 1º. Simular vector log-normal 
#Tamaño del vector
x1=lognrnd(0,1)
x2=lognrnd(0,1)
vx=[x1,x2]

sig11=
sig12=
sig21=
sig22=

A=[sig11,sig12;sig21,sig22]

# 2º. Aplicar transformación matricial Y=AX+mu

# 3º. Repetir paso 1 y 2 hasta optener todas las muestras deseadas

# 4º. Aplicar  las muestras a un problemas P.