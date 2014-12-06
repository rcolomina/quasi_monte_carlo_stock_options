#ifndef __SISTEMATRADING_H__

#include <list>
#include <iostream>
#include <map>

#include "parametros.h"

using namespace std;

class Candle{
	public:
	  Candle(int idReg,string fecha,double open,double high,double low,double close,string nombre):
			 idReg(idReg),fecha(fecha),open(open),high(high),low(low),close(close),nombre(nombre){}
	  Candle():idReg(0),fecha(string("")),open(0),high(0),low(0),close(0),nombre(string("")){}

	  double getOpen();
	  double getHigh();
	  double getLow();
	  double getClose();

	  list<Candle> getSubCandles();
	private:
	  int idReg; //identificador del tipo de registro
	  string fecha; //clave unica del registro
	  e_TimeFrame timeFrame;
	  double open;
	  double high;
	  double low;
	  double close;
	  string nombre;	  
	  list<Candle> subCandles; //asi se pueden contener subframes
};

//TODO: Derivar tipos de Candles, particulares


// Clases de conjuntos. Esto permite restringir las operaciones. 
// 1. No se puede hacer Training de un modelo mas que en TrainingSet
// 2. Elección de parámetros del modelo en CrossValidationSet
// 3. Pruebas del modelo en TestSet

class Set;
class TrainingSet;
class CrossValidationSet;
class TestSet;

//Crear operaciones de ordenacion entre fecha. ¿Quien es mas antigua?, 
class Fecha{
	public:
	  Fecha():minuto(1),hora(1),dia(1),mes(1),ano(2000){}
	  Fecha(int dia,int mes,int ano):minuto(1),hora(1),dia(dia),mes(mes),ano(ano){}
	  Fecha(string cadenaFecha):cadenaFecha(cadenaFecha){}
	  string get_fecha(e_FormatoFecha formato);
	  string get_cadenaFecha(){return cadenaFecha;}

	  string getFechaFormatoYYYYMMDD();
	  string getFechaFormatoDDMMYYYY();
//	  string getFechaFormato
	private:
	  int minuto;
	  int hora;
	  int dia;
	  int mes;
	  int ano;
	  string cadenaFecha;
};

class RegistroTrading{
	public:
	  RegistroTrading(const Candle &candle):candle(candle){}
	  RegistroTrading():fecha(Fecha()),candle(Candle()){}

	  Candle get_candle(){return candle;}

	  string imprimirRegistro();
	  double getPrecioMedio();

	  //double 
	private:
	  Fecha fecha;
	  e_TimeFrame frame;
	  Candle candle;
	  double volumen;
};

//Pasar a estructura?. Las ventajas de ser una clase, es que mantiene la coherencia de los
//valores de sus componentes, ya que solo se pueden setear en la construccion si se quiere así
// COMPRA-VENTA,  CORTO-COVERTURA
class RegOperacion{
	public:
	  RegOperacion(double precio,e_Ticker ticker,Fecha fecha,e_Operacion tipo,e_OLHC olhc):
			 precio(precio),ticker(ticker),fecha(Fecha()),tipo(tipo),olhc(olhc){}

	  double get_precio(){return precio;}
	  e_Ticker get_ticker(){return ticker;}
	  Fecha get_fecha(){return fecha;}
	  e_Operacion get_tipoOperacion(){return tipo;}
	  e_OLHC get_olhc(){return olhc;}
   private:
	  double precio;    //precio promedio realizado
	  e_Ticker ticker;  //ticker del valor
	  Fecha fecha;      //momento de la operacion
	  e_Operacion tipo; //tipo de operaicon
	  e_OLHC olhc;      //donde se ha realizado
};

class EstrategiaGestionCapital{
	public:
	  EstrategiaGestionCapital(){}
};

typedef map<string,bool> MapSignals;
typedef map<string,RegistroTrading> MapRegTrading;
typedef map<string,RegOperacion> MapRegOperaciones;
typedef list<RegistroTrading> ListRegTrading;


inline list<double> tomarListaValores(const e_OLHC &olhc,const MapRegTrading  &mapReg){
	  list<double> lista_valores;
	  
	  if(olhc==OPEN);			 
	  if(olhc==LOW);
	  if(olhc==HIGH);
	  if(olhc==CLOSE);
			 
	  return lista_valores;
}

//Se crean la estadistica con las operaciones construyéndolas con un mapa de operaciones
class EstadisticasTrading {
	public:
	  EstadisticasTrading(MapRegOperaciones operaciones):operaciones(operaciones){}

	  void imprimirInforme();
	  
	  
	private:
	  MapRegOperaciones operaciones;

};

class SistemaTrading {
	public:
     virtual MapSignals crearCompras(const MapRegTrading &registrosTrading)=0;
     virtual MapSignals crearCompras(const ListRegTrading &registrosTrading)=0;
 
     virtual MapSignals crearVentas(const MapRegTrading &registrosTrading)=0;
     virtual MapSignals crearCortos(const MapRegTrading &registrosTrading)=0;
     virtual MapSignals crearCubiertas(const MapRegTrading &registrosTrading)=0;
	  virtual MapRegOperaciones backtestingLargos(const MapRegTrading &registrosTrading,
																 const Fecha &fechaInicio,
																 const Fecha &fechaFin,
																 const double &comisiones,
																 const EstrategiaGestionCapital &estrategia,
																 const e_OLHC &olhc)=0;
 	 
};

class CruceMediasMoviles : public SistemaTrading {

	public:
	  CruceMediasMoviles(int media1,int media2):media1(media1),media2(media2){}
	  ~CruceMediasMoviles(){}

     MapSignals crearCompras(const MapRegTrading &mapRegistrosTrading);
     MapSignals crearCompras(const ListRegTrading &listaRegistrosTrading){return MapSignals();}

     MapSignals crearVentas(const MapRegTrading &registrosTrading){return MapSignals();}
  	  MapSignals crearCortos(const MapRegTrading &registrosTrading){return MapSignals();}
     MapSignals crearCubiertas(const MapRegTrading &registrosTrading){return MapSignals();}

	  MapRegOperaciones backtestingLargos(const MapRegTrading &registrosTrading,
													  const Fecha &fechaInicio,
													  const Fecha &fechaFin,
													  const double &comisiones,
													  const EstrategiaGestionCapital &estrategia,
													  const e_OLHC &olhc){return MapRegOperaciones();}


	private:
	  int media1;
	  int media2;
};



#endif
