#include <iostream>
#include "search.h"
using namespace std;

int main(){
float alist[10] = {1., 3., 5., 7., 11, 19., 21., 32., 43., 55.};
float target_value = 43.;
int high = sizeof(alist)/sizeof(alist[0])-1;
int low  = 0;
//Search* d(10);
Search * d;
d = new Search(10);
//int m = binarysearch(alist, target_value, 0, high);
//int m = interpolationsearch(alist, target_value, 0, high);
int m = d->binary(alist, target_value, low, high);
printf("binary search: Solution is %d  %f\n", m, alist[m]);
int m1 = d->interpolation(alist, target_value, 0, high);
printf("interpolation: Solution is %d  %f\n", m1, alist[m1]);
int m2 = d->linear(alist, target_value, 0, high);
printf("linear: Solution is %d  %f\n", m2, alist[m2]);
int step = 2;
int m3 = d->jump(alist, target_value, step);
printf("Jump: Solution is %d  %f\n", m3, alist[m3]);

int m4 = d->exponential(alist, target_value, sizeof(alist)/sizeof(alist[0]));
printf("exp search: Solution is %d  %f\n", m3, alist[m3]);

delete d;
return 0;
}
