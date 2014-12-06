#ifndef __ESTADISTICAS_H__

#include <iostream>
#include <map>
#include <list>
#include <math.h>

using namespace std;

// inline double sumatoria(const list<double> valores_x)
// inline double producto_escalar(const list<double> valores_x,const list<double> valores_y)
// inline double calcular_estadistico_x(const list<double> valores,const string estadistico) {
//inline double calcular_estadistico_xy(const list<double> valores_x,const list<double> valores_y,const string estadistico) {

inline double sumatoria(const list<double> valores_x){

	  list<double>::const_iterator it1=valores_x.begin();

	  if(valores_x.size() == 0)
			 return -1;

	  double suma_x=0;
	  while(it1 != valores_x.end()){
			 double x=*it1;
			 suma_x += x;
			 it1++;
	  }
     return suma_x;
}

inline double producto_escalar(const list<double> valores_x,const list<double> valores_y){

	  list<double>::const_iterator it1=valores_x.begin();
	  list<double>::const_iterator it2=valores_y.begin();

	  if(valores_x.size() != valores_y.size())
			 return -1;

	  double producto_escalar=0;
	  while(it1 != valores_x.end() && it2 != valores_y.end()){
			 
			 double x=*it1;
			 double y=*it2;

			 producto_escalar += x*y;

			 it1++;it2++;
	  }
	  return producto_escalar;
}

//Media
//Varianza
inline double calcular_estadistico(const list<double> valores,const string nombre_estadistico){

	  // Estimador de la media X
	  if(nombre_estadistico.compare("media")==0){
			 return sumatoria(valores)/valores.size();

	  // Estiamdor de la varancia X: (SigmaX)^2
	  } else if(nombre_estadistico.compare("varianza")==0){
			 double sumaCuadrados=producto_escalar(valores,valores);
			 double media=calcular_estadistico(valores,string("media"));
			 double n=valores.size();
			 return sumaCuadrados/n-media*media;
	  } else
			 return -1;

}


//Covarianza
//Covarianza-sesgada
//Pearson
inline double calcular_estadistico(const list<double> valores_x,const list<double> valores_y,const string nombre_estadistico) {

 	  if(valores_x.size() != valores_y.size())
			 return -1;

     // Estimador insesgado de la covarianza:  Sxy = 1 / (n-1) * Sigma(1,n) (Xi-muX) * (Yi-muY, donde muX y muY son media de X e Y
	  // Sxy = 1 / (n-1) * { Sum(Xi*Yi) - n Est.Media(X) * Est.Media(Y)) }
	  if(nombre_estadistico.compare("covarianza")==0){  

			 double media_x=calcular_estadistico(valores_x,string("media"));
			 double media_y=calcular_estadistico(valores_y,string("media"));
			 double n=valores_x.size();
			 return 1/(n-1) * (producto_escalar(valores_x,valores_y)-n*media_x*media_y);

	  }
	  else if(nombre_estadistico.compare("covarianza-sesgada")==0){  

			 double media_x=calcular_estadistico(valores_x,string("media"));
			 double media_y=calcular_estadistico(valores_y,string("media"));
			 double n=valores_x.size();
			 return 1/n * (producto_escalar(valores_x,valores_y)-n*media_x*media_y);

	  }
	  
	  // Estimador del coeficiente de correlacion de Pearson  RoXY = Sum(Xi*Yi)- n muX*muY / (n*Sx*Sy)
	  // Rxy = Sxy / (SigmaX * SigmaY)
	  else if(nombre_estadistico.compare("pearson")==0)
	  {
			 double covarianza=calcular_estadistico(valores_x,valores_y,string("covarianza"));
			 double desv_tip_x=sqrt(calcular_estadistico(valores_x,string("varianza")));
			 double desv_tip_y=sqrt(calcular_estadistico(valores_y,string("varianza")));

			 return covarianza / (desv_tip_x * desv_tip_y);
	  }
	  return -1;
}

#endif
