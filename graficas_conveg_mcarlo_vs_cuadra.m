
N=1000;
x=1:N;

y1=eye(N,1);
y2=eye(N,1);
y3=eye(N,1);
y4=eye(N,1);
y5=eye(N,1);

for i=1:N
  s1=2;s2=3;s3=4;s4=10;s5=20;

  y1(i)=i^(-1/s1);y2(i)=i^(-1/s2);y3(i)=i^(-1/s3);
  y4(i)=i^(-1/s4);
  y5(i)=i^(-1/s5);


endfor
 
hold on; 
plot(x,y1,'r');
plot(x,y2,'g');
plot(x,y3,'k');
plot(x,y4,'b');
plot(x,y5,'c');


xlabel('Numero de muestras');
ylabel('Error');


legend1=sprintf("s = %u",2);
legend2=sprintf("s = %u",3);
legend3=sprintf("s = %u",4);
legend4=sprintf("s = %u",10);
legend5=sprintf("s = %u",20);

legend(legend1,legend2,legend3,legend4,legend5);

ylabel("Error");
title("Orden de convergencia (s = dimension)");
legend('boxon');

print("order-convergencia.png");
