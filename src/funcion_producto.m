

# Prod( 1 + abs(hi)) con hi coorde de h en Z^s

h=[10,0,0,0,0];
norm(h)

prod=1;
for i=1:length(h)
	 prod = prod * (1+abs(h(i)));
endfor

power(prod,-2)