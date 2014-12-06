#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <sstream>
#include <regex>

#include <boost/iostreams/device/mapped_file.hpp>
#include <unordered_map>
#include "SistemaTrading.h"
#include "Estadisticas.h"

typedef unordered_map<int, string> work;

using namespace std;
using namespace boost::iostreams;

//Convertidor generico de Map a Vector
template <typename M, typename V> 
void MapToVec( const  M & m, V & v ) {
    for( typename M::const_iterator it = m.begin(); it != m.end(); ++it ) {
    	v.push_back( it->second );
    }
}



struct RegistroSpread{
	public:
	  RegistroSpread():fecha(string("")),cierre1(0),cierre2(0),nombre(string("")){}
	  int idRegistro; //identificador del tipo de registro
	  string fecha; //clave unica del registro
	  double cierre1;
	  double cierre2;
	  string nombre;
};


int main(int argc,char *argv[]){

	  bool test1=false;
	  bool test2=false;
	  bool test3=false;

	  if(argc!=2){
			 cout<<"Se acepta exactamente un argumento en entrada."<<endl;
			 return 1;
	  }
	  else
	  {																				 

			 ifstream fentrada(argv[1]);//,ifstream::in);
			 if(!fentrada.is_open()){
					cout<<"Nombre de fichero incorrecto o no encontrado."<<endl;
					return 1;
			 }
			 else
					cout<<"Abierto con exito fichero "<<argv[1]<<endl;

			 
			 //TODO: Determinar el tipo de registro con la cabecera
			 string cabecera;
			 getline(fentrada,cabecera);


			 map<string,RegistroSpread> mapRegistrosSpread;

			 while(!fentrada.eof()){
					stringstream ss;
					RegistroSpread registro;
					string line;

					getline(fentrada,line);
//					getline(fentrada,line);
					ss<<line;
					//Formato registro del fichero: fecha, double, double
					ss>>registro.fecha>>registro.cierre1>>registro.cierre2;

//					cout<<"Fecha:"<<registro.fecha<<" Cierre1:"<<registro.cierre1<<" Cierre2:"<<registro.cierre2<<endl;
					if(registro.fecha.compare(string(""))!=0)
						  mapRegistrosSpread[registro.fecha]=registro;
					
					//	getline(fentrada,line);
			 }


//TEST1: Muestra de datos cargados en entrada de fichero
 if(test1){
		cout<<"-----------------------------------"<<endl;
		cout<<" Cominezo de datos cargados en map "<<endl;
		cout<<"-----------------------------------"<<endl;

		for(map<string,RegistroSpread>::iterator itReg=mapRegistrosSpread.begin();
			 itReg!=mapRegistrosSpread.end();
			 itReg++)
			  cout<<itReg->second.fecha<<" "<<itReg->second.cierre1<<" "<<itReg->second.cierre2<<endl;
						  

		cout<<"------------------------------"<<endl;
		cout<<" Fin de datos cargados en map "<<endl;
		cout<<"------------------------------"<<endl;
		cout<<"******"<<endl;
		cout<<"******"<<endl;
		cout<<"******"<<endl;
		cout<<"--------------------------------------"<<endl;
		cout<<" Estadística de datos cargados en map "<<endl;
		cout<<"--------------------------------------"<<endl;
 }


//TEST2: Probar funciones estadísticas

 if(test2){

		//Extraer dos lista de double's del map de entrada
		list<double> cierres1,cierres2;
		for(map<string,RegistroSpread>::iterator itReg=mapRegistrosSpread.begin();
			 itReg!=mapRegistrosSpread.end();
			 itReg++){						  
			  cierres1.push_back(itReg->second.cierre1);
			  cierres2.push_back(itReg->second.cierre2);													
		}
				  
		cout<<"Media de Cierres de 1: "<<calcular_estadistico(cierres1,string("media"))<<endl;
		cout<<"Media de Cierres de 2: "<<calcular_estadistico(cierres2,string("media"))<<endl;

		cout<<"Varianza de Cierres de 1: "<<calcular_estadistico(cierres1,string("varianza"))<<endl;
		cout<<"Varianza de Cierres de 2: "<<calcular_estadistico(cierres2,string("varianza"))<<endl;

		list<double> x,y;
		x.push_back(1);
		x.push_back(1);
		y.push_back(4);
		y.push_back(5);

		cout<<"Producto escalar de x e y:"<<producto_escalar(x,y)<<endl;
		cout<<"Covarianza de x e y:"<<calcular_estadistico(x,y,string("covarianza"))<<endl;
		cout<<"Coef.Pearson de x e y:"<<calcular_estadistico(x,y,string("pearson"))<<endl;

		cout<<"Producto escalar de cierres1 e cierres2:"<<producto_escalar(cierres1,cierres2)<<endl;
		cout<<"Covarianza de cierres1 e cierres2:"<<calcular_estadistico(cierres1,cierres2,string("covarianza"))<<endl;
		cout<<"Coef.Pearson de cierres1 e cierres2:"<<calcular_estadistico(cierres1,cierres2,string("pearson"))<<endl;

//TODO:  

// Funcion que acepte un map de precios indexado por fechas, devuelva la lista de precios ordenada por fecha.
// Funcion que acepte lista ordenada de n precios pi, y devuelva una lista ordenada de retorno ri de tamaño n-1.
// Función que acepte una lista de n retornos ri , un valor inicial v0, y devuelva el valor final vn despues de aplicar todos los retornos en orden.
// Función que acepte una lista de n retornos ri , un valor inicial v0, y devuelva una lista n-1 de valores vi.
// Función que acepte una lista de n pares (x,y), y devuelva la regresión lineal, alfa y beta o  interseccion y pendiente

 }

//TEST3: mmap de Boost IOStreams
 if(test3){
		

		char *nfile=argv[1];
		string nombre1(nfile);

//		cout<<nfile;
	 //Initialize the memory-mapped file
		//stream<mapped_file_source> asdfile;
 
		mapped_file_params  params;
        params.path = "map.dat";
        params.new_file_size = 100;
        params.mode = (std::ios_base::out | std::ios_base::in);
        boost::iostreams::mapped_file  mf;

		  mf.open(params);
        work w1;
        w1[0] = "abcd";
        w1[1] = "bcde";
        w1[2] = "cdef";

        work* w = static_cast<work*>((void*)mf.data());
        *w = w1;
        mf.close();



//		mapped_file_source(nombre1);
    //Read the entire file into a string
    //string fileContent(file.data(), file.size());
    //Print the string
	 //  cout << fileContent;
    //Cleanup
//    file.close();

 }


//TEST4: Creacion de señales de compra
 cout<<"COMIENZO TEST 4"<<endl;

 CruceMediasMoviles sistCruceMM(5,10);

 //Crear entrada mapRegTrading
 MapRegTrading mapTrading;
 
 int idRegistro=1;
 for(map<string,RegistroSpread>::iterator itReg=mapRegistrosSpread.begin();
	  itReg!=mapRegistrosSpread.end();
	  itReg++){						  

//   Necesito Fecha
//  RegistroTrading (Fecha,RegistroCandle(idRegistro,date,open,high,low,close,nombre))			  
			  
	   //Extraer fecha del string
		/*Fecha fecha;
		string parsed;

		string input=itReg->first;
		string delimitador='-';
		size_t pos =0;
		while((pos = input.find(delimitador)) != 

		stringstream input_stringstream(input);
		if(getline(input_stringstream,parsed,'-')){
			  cout<<parsed;
		}*/

/*		string token, mystring(itReg->first);
		list<string> datos;
		while(token != mystring){
			  token = mystring.substr(0,mystring.find_first_of("-"));
			  mystring = mystring.substr(mystring.find_first_of("-") + 1);
			  printf("%s ",token.c_str());
			  datos.push_back(mystring);
		}*/
//		Fecha fecha(idRegistro,0,0);
		string fecha=itReg->first;
		Candle regCandle(idRegistro,fecha,0,0,0,itReg->second.cierre1,string("ejemplo1"));
		RegistroTrading regTrading(regCandle);

		if(fecha.compare(string(""))!=0)
				  mapTrading[fecha]=regTrading;

		idRegistro++;
		}

 MapSignals signals=sistCruceMM.crearCompras(mapTrading);
 
 for(MapSignals::iterator it=signals.begin();it!=signals.end();it++){
		cout<<it->first<<" ";
		cout<<it->second<<endl;
			  }

}//FIN PROGRAMA
// cout<<"COMIENZO TEST 4"<<endl;


  return 0;
}//FIN MAIN

