#include <iostream>
class Vect{
public:
 Vect(int n);
 ~Vect();
private:
 int* data;
 int  size;
};
Vect::Vect(int n){
 size = n;
 data = new int[n];
}
Vect::~Vect(){
 delete [] data;
}
int main(){
Vect a(5);
/***
printf("size is %d \n", a);
for (int i=0; i <a.size; a++)
  a[i] = i;
***/
return 0;
}
	
