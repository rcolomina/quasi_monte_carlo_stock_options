function f_return=perio_function(t,parametro)

	  if(parametro==1)
			 f_return=3*power(t,2)-2*power(t,3); 
	  else if(parametro==2)
			 f_return=10*power(t,3)-15*power(t,4)+6*power(t,5); 
     else if(parametro==3)
			 f_return=35*power(t,4)-84*power(t,4)+70*power(t,6)-20*power(t,7); 
	  else f_return=0;
	  endif
	 endif
    endif

endfunction
