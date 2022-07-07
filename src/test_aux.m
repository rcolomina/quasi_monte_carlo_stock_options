

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

x=log(length(f_glp(7)));
for i=1:9
   x=[x,log(length(f_glp(7+i)))];
endfor

aux=6;
plot(x(1:aux),errores(1:aux,1),"-o;Polynomial-2;",
     x(1:aux),errores(1:aux,2),"-o;Polynomial-3;",
     x(1:aux),errores(1:aux,3),"-o;Polynomial-4;",
     x(1:aux),errores(1:aux,4),"-*;Sin1-Transform;",
     x(1:aux),errores(1:aux,5),"-*;Sin2-Transform;",
     x(1:aux),errores(1:aux,6),"-*;Sin3-Transform;",
     x(1:aux),errores(1:aux,7),"-x;Sin4-Transform;");
xlabel('Log(N)');
ylabel('Log(RMSE)');


