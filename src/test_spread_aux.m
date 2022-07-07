plot(log(vector_N),log(RMSE(:,1)),"-o;Polynomial-2;",
     log(vector_N),log(RMSE(:,2)),"-o;Polynomial-3;",
     log(vector_N),log(RMSE(:,3)),"-o;Polynomial-4;",
     log(vector_N),log(RMSE(:,4)),"-*;Sin1-Transform;",
     log(vector_N),log(RMSE(:,5)),"-*;Sin2-Transform;",
     log(vector_N),log(RMSE(:,6)),"-*;Sin3-Transform;",
     log(vector_N),log(RMSE(:,7)),"-x;Sin4-Transform;",
     log(vector_N),log(RMSE(:,8)),"-x;No Periodization;");
