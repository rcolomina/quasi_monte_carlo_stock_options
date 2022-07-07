vN=[1024];%,4096];
vP=[363,661];

vSigma=[0.2,0.3,0.4];

vK=[100,110,120];

mSalidaMC=zeros(6,6);
mSalidaHibrido=zeros(6,6);
mSalidaHalton=zeros(6,6);
mSalidaGLP=zeros(6,6);
mSalidaGLPPerioPol1=zeros(6,6);

for i=1:length(vN)
	 N=vN(i);
    param=vP(i);

	 for j=1:length(vSigma)
		sigma=vSigma(j)

		for k=1:length(vK)
		  K=vK(k);

		  test_lookback_option;

		  mSalidaMC(i*k,2*j-1)=valor_lookback_mc;
        mSalidaMC(i*k,2*j)=desviacion_estandard;

		  mSalidaHibrido(i*k,2*j-1)=val_lookback_qmc_hibrido_vandercorput;
		  mSalidaHibrido(i*k,2*j)=est_error_val_lookback_qmc_hibrido_vandercorput;

		  mSalidaHalton(i*k,2*j-1)=val_lookback_qmc_halton;
		  mSalidaHalton(i*k,2*j)=est_error_val_lookback_qmc_halton;

		  mSalidaGLP(i*k,2*j-1)=val_lookback_qmc_lr;
		  mSalidaGLP(i*k,2*j)=est_error_val_lookback_qmc_lr;

		  mSalidaGLPPerioPol1(i*k,2*j-1)=val_lookback_qmc_lr_perio;
		  mSalidaGLPPerioPol1(i*k,2*j)=est_error_val_lookback_qmc_lr_perio;
		  

       endfor
	 endfor
endfor 
