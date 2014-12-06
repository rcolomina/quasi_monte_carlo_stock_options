#Dimension del problema
dim=5;

# parametros GLP RANGO1
paramglpr1=[[512,151];[1024,363];[1536,297];[4096,661]];

numparam=2
N=paramglpr1(numparam,1);
param=paramglpr1(numparam,2);

glp=f_glp_ndim(N,dim,param);

#Periodiza los datos
parametro_perio=8;

datos_perio=zeros(N,dim);

for i=1:N
   datos_perio(i,:)=f_periodifica(glp(i,:),parametro_perio);
endfor

glp_modif=datos_perio;

#Barajeo de los datos
#for j=1:dim
#    permuta=f_permuta_aleatoria(N);
#    for i=1:N
#   	array(i,j)=glp(permuta(i),j);
#    endfor
#endfor
#glp=array;

# LDS HIBRIDO USANDO VAN DER CORPUT
#glp=f_van_der_corput_ndim(N,dim);

# HALTON
#glp=f_halton([2,3,5,7,11],N);

#INVERSION POR OCTAVE
glp_modif=stdnormal_inv(glp);

#INVERSION DE ACKLAM
#glp_modif=eye(N,5);
#for i=1:N-1
#	for j=1:dim
#       val=stdnormal_inv_acklam(glp(i,j));
#		 glp_modif(i,j)=val;
#   endfor
#endfor

# MULTIPLOT
subplot(dim,dim,1);
index=1;
for i=1:dim
	  for j=1:dim
 		  subplot(dim,dim,index);
		  index=index+1;
        if(i>j)
   		 plot(glp_modif(:,i),glp_modif(:,j),'.');	          
        endif
	  endfor
endfor

