#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define TRUE   1
#define FALSE  0

int binarysearch(float alist[], float target_value, int low,  int high);
int linearsearch(float alist[], float target_value, int low,  int high);
int jumpsearch(float alist[],   float target_value, int step, int size);
int interpolationsearch(float alist[], float target_value, int low, int high);
int exponentialsearch(float alist[], float target_value, int size);
int exponentialsearch_range(float alist[], float target_value, float iraise, int size);

int binarysearch(float alist[], float target_value, int low, int high){
 int m = (high-low)/2+low +(high-low)%2;
 //printf("%d \n", m);
 if (alist[m] == target_value) return m;
 else if (alist[m]<target_value) return binarysearch(alist, target_value, m+1, high);
 else if (alist[m]>target_value) return binarysearch(alist, target_value, low, m-1);
 return -1;
}

int linearsearch(float alist[], float target_value, int low, int high){
for (int i = low; i<high; i++)
	if (alist[i] == target_value) return i;
return -1;
}

int jumpsearch(float alist[], float target_value, int step, int size){
int nsteps = size/step;
int found  = 0;
int index  = -1;
for (int i=0; i<nsteps; i++){
 	if (alist[i*step]> target_value) 
 		found = 1;
 		index = i;
 		break;}
 if (found ==1){
 	int low  = (index-1)*step;
 	int high =  index*step;
 	return linearsearch(alist, target_value, low, high);
 	 }
    else 
    {
    int low  = index*step;
    int high = size;
    return linearsearch(alist, target_value, low, size);}
 return -1;
}

int interpolationsearch(float alist[], float target_value, int low, int high){
if (low ==high) return low; 
int m = low +(int)(((float)(high-low)+1)*(target_value-alist[low])/(alist[high]-alist[low]));
if (alist[m] == target_value) return m;
else if (alist[m] > target_value) return interpolationsearch(alist, target_value, low, m);
else return interpolationsearch(alist, target_value, m, high);
return -1;
}

int exponentialsearch_range(float alist[], float target_value, float iraise, int size){
  int index = (int) pow(2., iraise);
  if (index >= size) return iraise;
  else if (alist[index] == target_value) return iraise;
  else if (alist[index] < target_value){
  	iraise +=1;
  	return exponentialsearch_range(alist, target_value, iraise, size);}
  else return iraise;
}

int exponentialsearch(float alist[], float target_value, int size){
  int iraise = 0;
  iraise      = exponentialsearch_range(alist, target_value, iraise, size);
  int index   =  (int) pow(2., iraise);
  int index1  =  (int) pow(2., iraise-1);
  if (alist[index] == target_value) return index;
  else if (alist[index]>size) return binarysearch(alist, target_value, index1,  size);
  else binarysearch(alist, target_value, index1,  index);
  return -1;
  }
  
int main(){
float alist[10] = {1., 3., 5., 7., 11, 19., 21., 32., 43., 55.};
float target_value = 43.;
int high = sizeof(alist)/sizeof(alist[0])-1;
//int m = binarysearch(alist, target_value, 0, high);
//int m = interpolationsearch(alist, target_value, 0, high);
int m = exponentialsearch(alist, target_value, high);
printf("Solution is %d  %f\n", m, alist[m]);
return 0;
}
