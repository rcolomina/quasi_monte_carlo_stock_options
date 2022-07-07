

puntos=500;
dim=5;
dx=0.1;

discrepa=eye(puntos,1);
for l=2:puntos-1

  glp=f_glp_ndim(puntos,dim,l);

  discrepa(l)=f_discrepancia_lattice_aprox(glp,dx);

endfor


discrepa

