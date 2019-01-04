#include <iostream>
#include <string>

class Search{
public:
   Search(int size);
   int nsize;
   int binary(float arr[], float target_value, int low, int high);
   int linear(float arr[], float target_value,  int low, int high);
   int jump(float arr[], float target_value, int step);
   int interpolation(float arr[], float target_value, int low, int high);
   int range(float arr[], float target_value, int iraise);
   int exponential(float arr[], float target_value, int size);
	
};