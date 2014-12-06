

function f_result=f_discrepancia_lattice_aprox(glp,dx)


  dim=length(glp(1,:));
  numpuntos=length(glp(:,1));

  cubo=eye(dim,1);
  cubo(:)=dx;
  normcubo=norm(cubo);

  puntos_dentro=0;
  for i=1:numpuntos
    punto=glp(i,:);

    if(norm(punto)<normcubo)
		puntos_dentro=puntos_dentro+1;
	 endif	
  endfor


  f_result=abs(puntos_dentro/numpuntos-power(dx,dim));


endfunction
