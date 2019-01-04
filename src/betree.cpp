#include <iostream>
using namespace std;

struct node{
 int val;
 struct node *left, *right;
  node(int val)
  {
   this->val    = val;
   left = right = NULL;
  }
};

void print_inorder(struct node* node){

 if (node == NULL)
 	return; 
 print_inorder(node->left);
 cout<<"  "<<node->val<<endl;
 print_inorder(node->right);
 
}

void print_postorder(struct node* node){
if (node == NULL)
 	return; 
 print_postorder(node->left);
 print_postorder(node->right);
 cout<<"  "<<(*node).val<<endl;
}

void print_preorder(struct node* node){
 if (node == NULL)
 	return; 
 	cout<<"   "<<node->val<<endl;
 	print_preorder(node->left);
 	print_preorder(node->right);
}
int main(){
struct node * root = new node(1);
root->left         = new node(2);
root->right        = new node(3);
root->left->left   = new node(4);
root->left->right  = new node(5);
cout<<"In order traversal: \n"<<endl;
print_inorder(root);
cout<<"Post order traversal: \n"<<endl;
print_postorder(root);
cout<<"Pre order traversal: \n"<<endl;
print_preorder(root);
return 0;
}