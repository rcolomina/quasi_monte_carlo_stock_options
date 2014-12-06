
n=100000;
vgauss=1:n;
for i=1:n
    vgauss(i)=stdnormal_inv(rand);
endfor
  
