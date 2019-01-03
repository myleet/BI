#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define TRUE   1
#define FALSE  0

void topdown_mergesort(int arrA[], int arrB[], int nsize);
void topdown_splitmerge(int arrB[], int ibegin, int iend, int arrA[]);
void topdown_merge(int arrA[], int ibegin, int imiddle, int iend, int arrB[]);

int main() {
int arrA[10] = {9, 10, 7, 3, 2, 4, 1, 5, 8, 11 };
int arrB[10];
int nsize = sizeof(arrA)/sizeof(arrA[0]);

topdown_mergesort(arrA, arrB, nsize);

for (int i =0; i<10; i++)
	printf(" %d \n", arrA[i]);
return 0;

}

void topdown_mergesort(int arrA[], int arrB[], int nsize){
for (int i =0; i<nsize; i++)
      arrB[i] = arrA[i];
topdown_splitmerge(arrB, 0, nsize, arrA);
}

void topdown_splitmerge(int arrB[], int ibegin, int iend, int arrA[]){
if ((iend-ibegin)<2) return;
else {int imiddle = (iend+ibegin)/2;
     topdown_splitmerge(arrA, ibegin, imiddle, arrB);
     topdown_splitmerge(arrA, imiddle,iend,    arrB);
     topdown_merge(arrB,  ibegin, imiddle, iend, arrA);}
    return;
}
void topdown_merge(int arrA[], int ibegin, int imiddle, int iend, int arrB[]){
  int i = ibegin;
  int j = imiddle;
  for (int k =ibegin; k<iend; k++){
      if ((i<imiddle) && ((j>=iend) || (arrA[i]<=arrA[j]))) {
         arrB[k] = arrA[i];
         i+=1;}
      else { 
        arrB[k] = arrA[j];
  		j +=1;}
  	}
   return;
}


