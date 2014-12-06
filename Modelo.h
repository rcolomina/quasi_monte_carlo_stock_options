#ifndef __MODELO_H__

template<typename T,typename M>
class FuncionCoste{
	  virtual T operator()(const M &muestra)=0;
};

class FuncionRealVariableReal : public FuncionCoste<double,double>{
		  public:
			 FuncionRealVariableReal(){}
	       double operator()(const double &valor);
};



/*
class GradienteFuncionCoste<T>{
	  virtual T calcular(M muestra);
};*/

/*
class Modelo;
class RegresionLineal : public Modelo;
class RegresionLogistica : public Modelo;
class RegresionMultilineal : public Modelo;
class AnalisisCluster : public Modelo;
*/

#endif
