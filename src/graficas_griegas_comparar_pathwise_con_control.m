legend1=sprintf("SIN control");
legend2=sprintf("CON control");

legend(legend1,legend2);
legend('boxon');

title("Comparativa de la evolucion de los estimadores MC de tipo pathwise,\n con y sin control, para la griega Delta de una opcion Call Europea.");
xlabel("Numero de muestras");
ylabel("Estimacion para Delta");
print("comparativa-delta-estimador-pathwise-con-sin-control.png");
