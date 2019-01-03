#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define TRUE   1
#define FALSE  0

int partition(int  A[], int low, int high);
void quicksort(int A[], int low, int high);

int main() {

int arr[10] = {9, 10, 7, 3, 2, 4, 1, 5, 8, 11 };
int low   = 0;
int high  = 9;

quicksort(arr, low, high);
for (int i =0; i<10; i++)
	printf(" %d \n", arr[i]);
return 0;
}

void quicksort(int arr[], int low, int high){
if (low<high){
    int pi = partition(arr, low, high);
    quicksort(arr,  low,  pi-1);
    quicksort(arr,  pi+1, high);
   }
}
int partition(int arr[], int low, int high){
  int pivot = arr[high];
  int i = low -1;
  for (int j =low; j<high; j++){
  	if (arr[j]<=pivot) {
  		i +=1;
  		int temp = arr[i];
  		 arr[i]  = arr[j];
  		 arr[j]  = temp;}
  	  }
   if (i+1!=high){
   	int temp  = arr[i+1];
   	arr[i+1]  = arr[high];
   	arr[high] =  temp;}
   	return i+1;
}