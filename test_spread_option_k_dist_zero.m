### CALCULA APROXIMACIONES DEL VALOR DE SPREAD OPTIONS PARA EL CASO GENERAL K distionto CERO
# INPUTS
# w1,w2 : pesos
# K : precio de ejercicio
# N : numero grande QMC referencia
# conjunto de parametros, S10, sigma1, T, ro
# S10 : precio inicial primer activo
# sigma1 : volatilidad primer activo
# T : perido de vida
# ro : coeficiente de correlacion entre S1 y S2
# rate : tipo de interes
# sigma2 : volatilidad segundo activo
# S20 : precio inicial segundo activo

# OUTPUTS
# Valoraciones de Spread Option para diferentes valores
# de tam. muestral y forma de periodizacion

# pesos de la spread option
w1=w2=1;

# relajar condicion K distinto de zero
K=100;

# numero de muestras QMC referencia teorica 
N=121393;

# conjuntos 1 de parametros: 144 casos
#vector_S10=[92,96,100,104];   # 4 casos
#vector_sigma1=[0.1,0.2,0.3]   # 3 casos
#vector_T=[7/364,30/365,1,5];  # 4 casos : 1 semana, 1 mes, 1 anho, 5 anhos
#vector_ro=[-0.5,0,0.5];       # 3 casos

# conjunto 2 de parametros: 16 casos
#vector_S10=[92,104];      # 2 casos
#vector_sigma1=[0.3]   # 2 casos
#vector_T=[1/12];      # 2 casos : 1 mes, 1 anho
#vector_ro=[-0.5];     # 2 casos

# conjunto 3 de parametros: 24 casos
#vector_S10=[92,104];      # 2 casos
#vector_sigma1=[0.1,0.3];   # 2 casos
#vector_T=[1/12,1,5];      # 3 casos : 1 mes, 1 anho, 5 anhos
#vector_ro=[-0.5,0.5];     # 2 casos

vector_S10=[104];      # 1 casos
vector_sigma1=[0.1];   # 1 casos
vector_T=[5];      # 1 casos : 1 mes, 1 anho, 5 anhos
vector_ro=[0.5];     # 1 casos


# parametros fijos
rate=0.1;
sigma2=0.2;
S20=100;
delta1=delta2=0.05;

# glp dimension 2 fibo. tamanho 121393 puntos
m=26;
glp_big=f_glp(m);

#################################################################################

numero_casos=length(vector_S10)*length(vector_sigma1)*length(vector_T)*length(vector_ro);

# arrancar reloj t0
t0=clock();

# reservar memoria
qmc_n_grande=zeros(numero_casos,1);
num_tam_glp=10;
num_param_perio=7;

valor_opciones=zeros(num_tam_glp,num_param_perio,numero_casos); # (tamanho glp, tipo periodiza, casos)

# bucle para calcular valor teoricos y aproximados
conta=1;
for i=1:length(vector_S10)
  for j=1:length(vector_sigma1)
	 for k=1:length(vector_T)
		for l=1:length(vector_ro)
		    S10=vector_S10(i);
			 sigma1=vector_sigma1(j);
			 T=vector_T(k);			 
			 ro12=vector_ro(l);
			 
			 ### CALCULAR LOS VALORES DE REFERENCIA TEORICAS PARA EL CONJUNTO DE PARAMETROS
			 qmc_n_grande(conta)=spread_option(glp_big,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T);
			 ###

			 ### CALCULAR UN VALOR APROXIMADOS SEGUN TAM. MUESTRA Y TIPO PERIODIZACION
		    for n=1:num_tam_glp
			   glp=f_glp(n+6);
			   for param_perio=1:num_param_perio
				  qmc_n=spread_option_periodifica(glp,w1,w2,rate,K,S10,S20,delta1,delta2,sigma1,sigma2,ro12,T,param_perio);
				  param_perio;
				  log_long_glp=log(length(glp));

				  valor_opciones(n,param_perio,conta)=qmc_n;

				 endfor
			 endfor
			 #######
			 conta++;
		endfor
	 endfor
  endfor
endfor

# tomar tiempo t0
elapse_time_t0=etime(clock(),t0)

### CALCULAR RMSE PARA POR COLUMNAS DE MATRIZ valor_opciones
errores=zeros(num_tam_glp,num_param_perio);
for i=1:num_tam_glp
  for j=1:num_param_perio
	      sumerror=0;
			for k=1:numero_casos
 			   sumerror+=f_error(valor_opciones(i,j,k),qmc_n_grande(k));
			endfor				
 	      errores(i,j)=log(sqrt(sumerror/numero_casos));
  endfor
endfor

### PINTANDO GRAFICAS DEL ERROR
x=log(length(f_glp(7)));
for i=1:9
   x=[x,log(length(f_glp(7+i)))];
endfor
aux=8;
plot(x(1:aux),errores(1:aux,1),"-o;Polynomial-2;",
     x(1:aux),errores(1:aux,2),"-o;Polynomial-3;",
     x(1:aux),errores(1:aux,3),"-o;Polynomial-4;",
     x(1:aux),errores(1:aux,4),"-*;Sin1-Transform;",
     x(1:aux),errores(1:aux,5),"-*;Sin2-Transform;",
     x(1:aux),errores(1:aux,6),"-*;Sin3-Transform;",
     x(1:aux),errores(1:aux,7),"-x;Sin4-Transform;");
xlabel('Log(N)');
ylabel('Log(RMSE)');







