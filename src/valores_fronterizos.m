
for(i=1:length(glp))
			if(glp(i,1)>0.999)
            glp(i,1)
         endif
		   if(glp(i,2)>0.999)
            glp(i,2)
         endif
			if(glp(i,1)<0.001)
            glp(i,1)
         endif
		   if(glp(i,2)<0.001)
            glp(i,2)
         endif

 endfor
		 
