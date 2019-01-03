#include <stdio.h>
#include <stdlib.h>
#include <math.h>

struct node{
 int val;
 struct node * left;
 struct node * right;
 };

struct node* newNode(int val){
  struct node* node = (struct node*)malloc(sizeof(struct node));
  node->val   = val;
  node->left  = NULL;
  node->right = NULL;
  return (node); 
}

void print_inorder(struct node* node){

 if (node == NULL)
 	return; 
 print_inorder(node->left);
 printf("%d   \n", node->val);
 print_inorder(node->right);
}
void print_postorder(struct node* node){
if (node == NULL)
 	return; 
 print_postorder(node->left);
 print_postorder(node->right);
 printf("%d   \n", node->val);

}
void print_preorder(struct node* node){
 if (node == NULL)
 	return; 
 	printf("%d   \n", node->val);
 	print_preorder(node->left);
 	print_preorder(node->right);
}

int main(){
struct node * root = newNode(1);
root->left         = newNode(2);
root->right        = newNode(3);
root->left->left   = newNode(4);
root->left->right  = newNode(5);
printf("In order traversal: \n");
print_inorder(root);
printf("Post order traversal: \n");
print_postorder(root);
printf("Pre order traversal: \n");
print_preorder(root);
return 0;
}