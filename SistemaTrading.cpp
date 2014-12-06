#include "SistemaTrading.h"

MapSignals CruceMediasMoviles::crearCompras(const MapRegTrading &regT){

	  //Extraer una lista a parteir del MapRegTrading

	  //Calcular serie1
	  //list<double> serie1=
	  //Calcular serie2

	 		 //Comprobar que los parámetros media1 y media2 son menores que numero de registrosTrading
			 //Iterar registrosTrading
			    //En el momento en el que se puedan calcular todos los indicadores con historial del pasado
			    //Calcular indicadores media1 k1 y media k2 desde el momento max(k1,k2)<n en 1:n
			    //Examinar condicion de cruce alcista
			    //Añadir señal al mapa de señales en salida			
	  MapSignals signals;

	  for(MapRegTrading::const_iterator itReg=regT.begin();itReg!=regT.end();itReg++){
			 string fecha=itReg->first;

			 signals[fecha]=true;
	  }
 
			 return signals;
}


/*mapRegOperaciones CruceMediasMoviles::backtestingLargos(const mapRegTrading &registrosTrading,
													  const Fecha &fechaInicio,
													  const Fecha &fechaFin,
													  const double &comisiones,
													  const EstrategiaGestionCapital &estrategia,
													  const e_OLHC &olhc){


			 //Extraer los registros de trading entre las fecha indicadas
			 //Crear compras y ventas en el periodo
			 //Recorrer señales de compra y venta
			 //Reglas: 2 estados, comprado/liquidez
			 // Si liquidez, no se atiende a la señal de venta, se atiende a la señal de compra.
			 // Si comprado, no se atiende a la señal de compra, se atiende a la señal de venta.
			 //      Cuando se realice la venta, calcular la operacion generada con la señal de venta y la ultima señal de compra.
			 //      Añadir RegistroOperacion al mapa de salida

			 return mapRegOperaciones();
}*/
