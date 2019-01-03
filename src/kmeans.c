#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define TRUE   1
#define FALSE  0

float   rand_number(float scale);
float * compute_centroid(float * coordinates, int * assignment, int k, int dim, int ndat);
int   * compute_assignment(float * coordinates, float * centroid, int ndat, int k, int dim);
int   * initialize_assignment(int ndat, int k);

int main() {
  int i, j;
  printf("Kmeans in C \n");
  unsigned int ndat = 100;
  int   k  = 4;
  int dim  = 2;
  float *centroid = malloc(sizeof(float)*k*dim);
  
  for (i=0; i<k; i++)
  	for (j=0; j<dim; j++)
  		*(centroid +i*dim+j) = (float)i+(float)j;
  		
    for (i=0; i<k; i++)
  		for (j=0; j<dim; j++)
  			if (j==0) printf("( %f ",*(centroid +i*dim+j));
  			else printf(" %f  ) \n",*(centroid +i*dim+j));
  printf("-------------------------------\n");
  			
  float scale        = 2.0 ; 
  float *coordinates = malloc(sizeof(float)*ndat*dim);
  
  for (i = 0; i<ndat; i ++)
  	 for (j = 0; j<dim; j++)
  		  *(coordinates+((i*dim)+j)) =  *(centroid +(i%k)*dim+j) + scale*rand_number(scale);
  
  
   for (i = 0; i<ndat; i ++)
  	 for (j = 0; j<dim; j++)
  	    if (j==0) printf("( %f ",*(coordinates +i*dim+j));
  		else printf(" %f  ) \n",*(coordinates  +i*dim+j));
  		
   printf("  ======================================== \n" );  	
   int * assi = initialize_assignment(ndat, k);
   centroid   = compute_centroid(coordinates, assi, k, dim, ndat);
   for (i = 0; i<k; i++)
   	for (j =0; j<dim; j++) 
   	    if (j==0) printf("( %f ",*(centroid +i*dim+j));
  		else printf(" %f  ) \n",*(centroid +i*dim+j));
   printf(" ------------------------------------------ \n" ); 
  assi = initialize_assignment(ndat, k);
  centroid   = compute_centroid(coordinates, assi, k, dim, ndat);
   for (i = 0; i<k; i++)
   	for (j =0; j<dim; j++) 
   	    if (j==0) printf("( %f ",*(centroid +i*dim+j));
  		else printf(" %f  ) \n",*(centroid +i*dim+j));
  //*****************************************************************
   int iter = 0 ;
   assi = initialize_assignment(ndat, k);
   while (iter <10) {
   	   printf(" %d ============================== \n", iter);  		
	   centroid = compute_centroid(coordinates, assi, k, dim, ndat);
		for (i = 0; i<k; i++)
		   for (j = 0; j<dim; j++)
			  if (j==0) printf("( %f ",*(centroid + i*dim+j));
			  else      printf(" %f  ) \n",*(centroid +i*dim+j));
	   printf("-------------------------------------- \n");
	   assi = compute_assignment(coordinates, centroid, ndat, k, dim);
	   //for (i=0; i<ndat; i++)
	   //		printf(" %d     %d \n", i, *(assi+i));
	   iter +=1;
  }
  free(centroid);
  free(coordinates);
  printf("Kmeans is done. \n");
}

float rand_number(float scale) {
	 int low  =   0;
	 int high = 100;
	 return (float)(rand()%(high-low+1)+low)/(float)(high-low+1)*scale;
}
	
float * compute_centroid(float * coordinates, int * assignment, int k, int dim, int ndat) {	
   float * arr  = malloc(sizeof(float)*k*dim);
   float * arr1 = malloc(sizeof(float)*k);
   
   for (int i = 0; i<k; i++)
	   for (int j = 0 ; j <dim; j++){
	   		*(arr+i*dim+j) = 0.0;
	   		*(arr1+i)      = 0.0;
	   		}
	for (int i = 0; i<ndat; i++)
		for (int l = 0; l<k; l++)
	     if (*(assignment+i) == l){
	     	*(arr1 +l) += 1.0;
	        for (int j = 0 ; j <dim; j++)
	   	  	     *(arr+l*dim+j) += *(coordinates+i*dim+j);}
	   	  	     
	for (int i = 0; i<k; i++)
	   for (int j = 0 ; j <dim; j++){
	   		if (*(arr1+i)!= 0.0)
	   	       *(arr+i*dim+j)/= *(arr1+i);
    }
    free(arr1);
    return arr;
 }
int * compute_assignment(float * coordinates, float * centroid, int ndat, int k, int dim) {
  int * assignment = malloc(sizeof(int)*ndat);
  for (int i = 0; i<ndat; i++){
  	 double dmin   = HUGE_VAL;
  	 *(assignment+i) = -1;
     for (int l = 0; l<k; l++){
  	      double dis = 0.0;
          for (int j=0; j <dim; j++){
  			 dis += pow((double)(*(coordinates+i*dim+j)-*(centroid+l*dim+j)), 2.0);
  			 if (dis<dmin){
  			 	dmin = dis;
  			 	*(assignment+i) = l;}
		 }
	 }	
  }
 	return assignment;
}
int * initialize_assignment(int ndat, int k){
	int high =  k;
	int low  =  0;
	int * assignment = malloc(sizeof(int)*ndat);
	for (int i = 0; i<ndat; i++)
		*(assignment+i) = rand()%(high-low)+low;
	return assignment;
}