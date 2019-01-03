// Example simple Kmeans
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

void swap(int *a, int *b)
{
   int temp = *a;
   *a  = *b;
   *b  = temp;
}
void randomize_assignment(int arr[], int n, int k) {
   srand(time(NULL));
   for (int i = 0; i<n; i++) {
      arr[i] = rand()%k;
   }
}
void shake_coord(float** arr, int n, int shake){
	srand(time(NULL));
	for (int i = 0; i<n; i++){
		float perturbation0 = (rand()%100)/100.*shake;
		float perturbation1 = (rand()%100)/100.*shake;
		arr[i][0] +=perturbation0*pow(-1., rand()%100);
		arr[i][1] +=perturbation1*pow(-1., rand()%100);
	}
}
float* compute_centroid(float** coord, int* assign, float** centroid, int n, int k){
 for (int i =0; i<k; i++){
 	   float xc = 0.0;
 	   float yc = 0.0;
 	   int nc   = 0;
 	   for (int j =0; j<n; j++) {
 	   		if (assign[j]==i) {
 	   			centroid[i][0] +=coord[j][0];
 	   			centroid[i][1] +=coord[j][1];
 	   			nc +=1; 
 	   	   }
 	    }
 	    if (nc!=0){
 	    centroid[i][0]  *=1./nc;
 	    centroid[i][1]  *=1./nc;
 	 }
  }
  return centroid;
}
float* compute_assign(float** coord, float** centroid, int* assign, int n, int k){
   float min_dis = 1.0e29;
   for (int i =0; i<k; i++){
   	 for (int j=0; j<n; j++){
		 float temp1  = coord[j][0]-centroid[j][0];
		 float temp2  = coord[j][1]-centroid[j][1];
		 float dis = sqrt(temp1*temp1+temp2*temp2);
		 if (dis<min_dis) {
			  min_dis   = dis;
			  assign[j] = i;
			 }
 	 }
  }
   return assign;
}
int main() {
  srand(time(NULL));
  printf("Simple K-means \n");
  int n    = 500;
  int k    = 5;
  int ndim = 2;
  float shake = 3.5;
  //------Define arrays
  float *coord[n];
  for (int i =0; i<n; i++)
       coord[i] = (float *)malloc(ndim*sizeof(float));
  // Initialization of coord
  for (int i=0; i<k; i++){
  	for (int j=0; j<n/k; j++){
  		  coord[j+i*n/k][0] = 1.0+j*3.;
  		  coord[j+i*n/k][1] = 2.0+j*3.;
  		 printf("%f  \n",     coord[i][0]);
  		 printf("%f  \n",     coord[i][1]);
  		}
   }
  	int *assign;
       assign = malloc(n*sizeof(int));
       
    for (int i =0; i<n; ++i)
       *assign++ = -1;
    //
    float *centroid[k];
      for (int i =0; i<k; i++)
          centroid[i] = (float *)malloc(ndim*sizeof(float));
          	
      for (int i =0; i<k; i++){
         for (int j =0; j<ndim; j++)
    	 centroid[i][j] = 0.0;	    
      }
    //
    shake_coord(coord, n, shake);
    randomize_assignment(assign, n, k);
    int iter = 0;
    for (int i =0; i<8; i++){
       printf("%d \n ", assign[i]);
    }
    while (iter< 5)
     {
     	printf(" -------iteration  %d  \n", iter); 
    	float *centroid1 = compute_centroid(coord, assign, centroid, n, k);
    	float *assign1   = compute_assign(coord, centroid1, assign, n, k);
    	assign = assign1;
    
		for (int i =0; i<k; i++)
		  printf("%d  %f, %f  \n", i, coord[i][0], coord[i][1]);
		  iter +=1;	  
	  }
  	
  	free(coord);
  	free(assign);
  	free(centroid);
}