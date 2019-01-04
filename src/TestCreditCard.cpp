// Credit Card
#include "CreditCard.h"
#include <vector>
using namespace std;
void testCard(){
vector<CreditCard*> wallet(10);
 wallet[0] = new CreditCard("5391 0375 9387 5309", "John Bowman", 2500);
 wallet[1] = new CreditCard("3485 0399 3395 1954", "John Bowman", 3500);
 wallet[2] = new CreditCard("6011 4902 3294 2994", "John Bowman", 5000);
 
 for (int j =1; j<16; j++){
 wallet[0] ->chargelt(double(j));
 wallet[1] ->chargelt(2*j);
 wallet[2] ->chargelt(double(3*j));
 }
 cout<<"Card payments:\n";
 for (int i=0; i<3;i++){
   //cout << *wallet[i];
   while (wallet[i]->getBalance()>100.){
      wallet[i] -> makePayment(100.);
      cout<<" New ballance = " <<wallet[i]->getBalance()<<"\n";
        }
      cout<<"\n";
      delete wallet[i];
      }
}
int main(){
  testCard();
  return EXIT_SUCCESS;
  }
 