
dim=2;
num=10;

numpuntos=power(num,dim);
array=eye(numpuntos,dim);
array=f_variaciones_repeticion(num,dim);

totalvol=0;
for x=1:numpuntos
   vector=array(x,:);
   valf=f_hiperesfera_explicita_exacta(vector,1);
	vol=valf*power(1/num,dim);
   totalvol+=vol;
endfor


%volumen/=numpuntos
totalvol=volumen*power(2,dim+1)/numpuntos;
