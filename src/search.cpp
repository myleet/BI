#include <iostream>
#include "search.h"
using namespace std;

Search::Search(int size){

int nsize = size;
 printf("!!!nsize  %d \n", nsize);
}

int Search::binary(float arr[], float target_value, int low, int high){
  int m = low+(high-low)/2+(high-low)%2;
  if (arr[m]==target_value) return m;
  else if (arr[m]>target_value) return Search::binary(arr, target_value, low, m-1);
  else return Search::binary(arr, target_value, m+1, high);
}

int Search::linear(float arr[], float target_value, int low, int high){
 int m = -1;
 for (int i =low; i<high; i++)
 	if (arr[i] == target_value){
 		m = i;
 		break;}
  return m;
}
int Search::jump(float arr[], float target_value, int step){
   printf("nsize  %d \n", nsize);
  for (int i =0; i<nsize/step; i++){
  	 int m  =  i*step;
  	if (arr[m] > target_value) return Search::linear(arr, target_value, m-step, m);
  	else if (arr[m] == target_value) return m;
  	else return  Search::linear(arr, target_value, m, nsize -1);
   }
   return -1;
}
int Search::interpolation(float arr[], float target_value, int low, int high){
  int m = int(float(high-low+1)/(arr[high] - arr[low])*(target_value-arr[low])+0.5);
  if (low == high) return low;
  if (arr[m] == target_value) return m;
  else if (arr[m] < target_value) return Search::interpolation(arr, target_value, m, high);
  else return Search::interpolation(arr, target_value, low, m);
}

int Search::range(float arr[], float target_value, int iraise){
int index = 1<<iraise;
if (arr[index] > target_value)     return iraise;
else if (arr[index]==target_value) return iraise;
else {
   iraise +=1;
   return  Search::range(arr, target_value, iraise);}
}
int Search::exponential(float arr[], float target_value, int size){
  int iraise = 0;
  iraise = 	Search::range(arr, target_value, iraise);
  int index = 1<<iraise;
  if (arr[index] ==target_value) return index;
  else {
    int index1 = 1<<(iraise-1);
    int index2 = (index < size - 1 ? index : size-1);
    return Search::binary(arr, target_value, index1, index2);
  }
}
