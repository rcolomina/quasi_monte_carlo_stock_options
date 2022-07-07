# INVERSA NORMAL ESTANDAR (por ACKLAM)
# INPUTS
# p : percentil de la normal estandar en (0,1)
# Atencion con los valores proximos a 0 y 1.
# OUTPUS
# Valor de la funcion de distribucion normal estandard 
function f_return=stdnormal_inv_acklam(p)

   #Coefficients in rational approximations.

   a(1) = -3.969683028665376e1;
   a(2) = 2.209460984245205e2;
   a(3) = -2.759285104469687e2;
   a(4) = 1.383577518672690e2;
   a(5) = -3.066479806614716e1;
   a(6) = 2.506628277459239e0;

   b(1) = -5.447609879822406e+01;
   b(2) =  1.615858368580409e+02;
   b(3) = -1.556989798598866e+02;
   b(4) =  6.680131188771972e+01;
   b(5) = -1.328068155288572e+01;

   c(1) = -7.784894002430293e-03;
   c(2) = -3.223964580411365e-01;
   c(3) = -2.400758277161838e+00;
   c(4) = -2.549732539343734e+00;
   c(5) =  4.374664141464968e+00;
   c(6) =  2.938163982698783e+00;

   d(1) =  7.784695709041462e-03;
   d(2) =  3.224671290700398e-01;
   d(3) =  2.445134137142996e+00;
   d(4) =  3.754408661907416e+00;

  # Define break-points.
   p_low  = 0.02425;
   p_high = 1 - p_low;
  # Rational approximation for lower region.
  if((0 < p) && (p < p_low))
      q = sqrt(-2*log(p));
		aux1= ((((c(1)*q+c(2))*q+c(3))*q+c(4))*q+c(5))*q+c(6);
		aux2= ((((d(1)*q+d(2))*q+d(3))*q+d(4))*q+1);
      f_return =  aux1 / aux2;
   endif
  # Rational approximation for central region.
   if( (p_low <= p) && (p <= p_high))
      q = p - 0.5;
      r = q*q;
		aux1=(((((a(1)*r+a(2))*r+a(3))*r+a(4))*r+a(5))*r+a(6));
		aux2=(((((b(1)*r+b(2))*r+b(3))*r+b(4))*r+b(5))*r+1);
      f_return = aux1*q /  aux2; 
   endif
  # Rational approximation for upper region.
   if( p_high < p && p < 1)
      q = sqrt(-2*log(1-p));
		aux1=-(((((c(1)*q+c(2))*q+c(3))*q+c(4))*q+c(5))*q+c(6));
		aux2=((((d(1)*q+d(2))*q+d(3))*q+d(4))*q+1);
      f_return = aux1 / aux2;
   endif

endfunction
