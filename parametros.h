#ifndef __PARAMETROS_H___

enum e_FormatoFecha{
	  DMA,
	  AMD,
	  MDA,
	  YYYYMMDD,
	  DDMMYYYY,
	  MMDDYYYY,
	  YYYY_MM_DD,
	  DD_MM_YYYY,
	  MM_DD_YYYY
};

enum e_TimeFrame{
	  fSEMANAL,
	  fDIARIO,
	  fHORARIO,
	  f30MIN,
	  f15MIN,
	  f10MIN,
	  f5MIN,
	  f1MIN,
	  f1SEG
};

enum e_Operacion{
	  COMPRA,
	  VENTA,
	  CORTO,
	  CUBIERTA
};

enum e_OLHC{
	  OPEN,
	  LOW,
	  HIGH,
	  CLOSE
};

enum e_Ticker{
	  BBVA,
	  SAN,
	  TEF,
	  IDR
};

#endif
