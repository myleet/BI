#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define TRUE   1
#define FALSE  0

double   rand_number(double scale);
double * fcm_iters(double * data, int ndat, int k, int dim, int niter);
double * rand_uniform(double scale, int k, int ndat);
double * compute_distance(double * data, double * centroid, int ndat, int k, int dim);
double * compute_umat(double * dis, int ndat, int k, double m);
double * compute_centroid(double * umat, double * data, int ndat, int k, int dim, double m);

int main() {
	int ndat         = 200;
	int dim          = 3;
	int k            = 4;
	double * data    = malloc(sizeof(double)*ndat*dim);
	double *centroid = malloc(sizeof(double)*k*dim);
	double * umat    = malloc(sizeof(double)*ndat*k);
	int niter        = 30;
	double scale     = 1.0;
	
   printf("-------->>> Preset Centroids <<<---------\n");
  for (int i=0; i<k; i++)
  	for (int j=0; j<dim; j++)
  		*(centroid +i*dim+j) = (double)(i*i)+(double)(j*j);
  		
    for (int i=0; i<k; i++)
  		for (int j=0; j<dim; j++)
  			if (j==0) printf("( %lf ",*(centroid +i*dim+j));
  			else if (j==1) printf("  %lf ",*(centroid +i*dim+j));
  			else printf(" %lf  ) \n",*(centroid +i*dim+j));
  printf("--------->>> Shuffled Points around centroids <<<----------\n");
	
  for (int i = 0; i<ndat; i ++)
  	 for (int j = 0; j<dim; j++)
  		 *(data+((i*dim)+j)) =  *(centroid +(i%k)*dim+j) + scale*rand_number(scale);
  		 
  for (int i = 0; i<ndat; i ++)
  	 for (int j = 0; j<dim; j++)
  	    if (j==0) printf("( %lf ",*(data +i*dim+j));
  	    else if (j==1) printf(" %lf ",*(data +i*dim+j));
  		else printf(" %lf  ) \n",*(data  +i*dim+j));
  		
   printf("  ======================================== \n" );
    	
  printf("  ========>>>>>>> FCM <<<<<<<============ \n" );
  umat =  fcm_iters(data, ndat, k, dim, niter);
  free(centroid);
  free(data);
  free(umat);
  printf("Kmeans is done. \n");
}

double rand_number(double scale) {
	 int low  =   0;
	 int high = 100;
	 return (double)(rand()%(high-low+1)+low)/(double)(high-low+1)*scale;
}

double * rand_uniform(double scale, int k, int ndat){
	double * rlist = malloc(sizeof(double)*ndat*k);
	for (int l = 0; l<ndat; l++){
		double norm = 0.0L;
		for (int i=0; i<k; i++) {
			double rnum = rand_number(scale);
			*(rlist+l*k+i) = rnum;
			 norm += rnum;}
		for (int i=0; i<k; i++)
			*(rlist+l*k+i) /=norm;
	}
	return rlist;
}

double * compute_distance(double * data, double * centroid, int ndat, int k, int dim){
     double * dis = malloc(sizeof(double)*k*ndat);
     for (int i = 0; i<ndat; i++){
       for (int l = 0; l<k;  l++ )
       	  *(dis+i*k+l) = 0.0L;}
     	
          for (int i = 0; i<ndat; i++)
                for (int l =0; l<k; l++){
                	  double dis1 = 0.0L;
                	  for (int j =0; j<dim; j++){
                	     dis1 += pow(*(data+i*dim+j) - *(centroid+l*dim+j), 2.0);}
     		        *(dis+i*k+l) +=sqrt(dis1);}
 	return dis;
 }
 
 double * compute_umat(double * dis, int ndat, int k, double m){
 	double * umat = malloc(sizeof(double)*k*ndat);
 	for (int i = 0; i<ndat; i++)
 		for (int j =0; j<k; j++){
 		  double u = 0.0L;
 		  for (int l=0; l<k; l++){
 		      u += pow(*(dis+i*k+j)/(*(dis+i*k+l)), 2.0/(m-1.));}      
 		  *(umat+i*k+j) = 1./u; 
 	  }
 	return umat;
}
double * compute_centroid(double * umat, double * data, int ndat, int k, int dim, double m){
	double * centroid = malloc(sizeof(double)*k*dim);
	double * norm     = malloc(sizeof(double)*k*dim);
	double * denorm   = malloc(sizeof(double)*k);
	
	for (int i = 0; i<k; i++) {
	   *(denorm +i) = 0.0L;   
	   for (int j = 0; j<dim; j++)
	      *(norm+i*dim+j) = 0.0L;}
	
	   for (int i = 0; i<k;    i++)
		   for (int j= 0; j<ndat; j++)
			  *(denorm +i)    += pow(*(umat +j*k+i), m);
			  
	   for (int i = 0; i<k; i++)
		  for (int j= 0; j<ndat; j++)
		  	for (int l=0; l<dim; l++)  
			  *(norm+i*dim+l) += pow(*(umat +j*k+i), m)*(*(data +j*dim+l));
			   
		for (int i = 0; i<k; i++)		  
		    for (int j = 0; j<dim; j++)
	         *(centroid +i*dim + j) = (*(norm+i*dim+j))/(*(denorm + i));
  free(norm);
  free(denorm);
  return centroid;
}
double * fcm_iters(double * data, int ndat, int k, int dim, int niter){
	int i, j, l, iter = 0;
	double scale      = 2.0;
	double m          = 1.5;
    double * umat     = malloc(sizeof(double)*ndat*k);
    double * centroid = malloc(sizeof(double)*dim*k);
    double * dis      = malloc(sizeof(double)*ndat*k);
    umat              = rand_uniform(scale, k, ndat);
    printf("ndat=  %d   K = %d  m = %lf \n", ndat, k, m);
 
    while (iter < niter) {
		  printf("iter %d ========================== \n", iter);
		  centroid = compute_centroid(umat, data, ndat, k, dim, m);
		  printf(" ----->>>  Centroids <<<------ \n");
		  for (i =0; i<k; i++)
			for (j= 0; j<dim; j++)
				if (j==0) printf("( %lf ", *(centroid +i*dim+j));
				else if (j==1) printf(" %lf ", *(centroid +i*dim+j));
				else printf(" %lf )  \n", *(centroid +i*dim+j));
		  printf(" -------------------------------- \n");		
		  dis      = compute_distance(data, centroid, ndat, k, dim);
		  umat     = compute_umat(dis, ndat, k, m);
		  iter    +=1;
    }
    free(centroid);
    free(dis);
	return umat;
}