#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define TRUE   1
#define FALSE  0

// typical example  recursion

int factor(int n){
if      (n==0) return 1;
else if (n==1) return 1;
else return n*factor(n-1);
}

int main() {
for (int i =0; i<10; i++)
  printf(" %d! = %d  \n", i, factor(i));
}