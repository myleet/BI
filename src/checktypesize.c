#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define TRUE   1
#define FALSE  0
int main(){
int x = 1;
printf("integer %d size is  %lu   \n", x, sizeof(x));
float x1 = 1.;
printf("float number %f  size is  %lu   \n", x1, sizeof(x1));
double x2 = 1.L;
printf("double number %lf size is  %lu   \n", x2, sizeof(x2));
unsigned x3 = 1;
printf("unsigned integer size is  %lu   \n", sizeof(x3));
signed x5 = 1;
printf("signed integer %d size is  %lu   \n", x5, sizeof(x5));
long int x4 = 1;
printf("long integer %li size is  %lu   \n", x4, sizeof(x4));
long unsigned x6 = 1;
printf("long unsigned %lu size is  %lu   \n", x6, sizeof(x6));
char x7='m';
printf("char %c size is  %lu   \n", x7, sizeof(x7));
short int x8=1;
printf("short integer %d size is  %lu   \n", x8, sizeof(x8));
return 0;
}
