
N=200000;
rndunifset=eye(N,2);
for i=1:N
			  rndunifset(i,1)=fmod(unifrnd(0,1),1);
			  rndunifset(i,2)=fmod(unifrnd(0,1),1);
endfor

plot(rndunifset(:,1),rndunifset(:,2),"o");
