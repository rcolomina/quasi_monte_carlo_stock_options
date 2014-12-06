m=17;
param=1;
good_lattice_points;
seriex=f_periodifica(glp(:,1),param);
seriey=f_periodifica(glp(:,2),param);
#plot(seriex,seriey,"x",glp(:,1),glp(:,2),"o");
plot(seriex,seriey,"x");

snivx=stdnormal_inv(seriex);
snivy=stdnormal_inv(seriey);

#plot(snivx,snivy,"x");

for i=1:length(snivx)
			  if(snivx(i)<1.0e-6)
					 snivx(i);
           endif
endfor

for i=1:length(snivy)
			  if(snivy(i)<1.0e-6)
					 snivy(i);
           endif
endfor
