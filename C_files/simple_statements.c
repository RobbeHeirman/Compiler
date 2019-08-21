
#include <stdio.h>

int fibb(){

    int fib_arr[50];
    int n = 10;
    fib_arr[0] = 1;
    fib_arr[1] = 1;

    int k = 2;
    int next = 0;

    while(k < n){
    fib_arr[k] = fib_arr[k - 1] + fib_arr[k - 2];
    k = k + 1;


    char print_arr[4];
    print_arr[0] = '%';
    print_arr[1] = 'i';
    print_arr[2] = ' ';
    print_arr[3] = '\0';

    char* print_ptr = &print_arr[0];
    printf(print_ptr, fib_arr[k - 1]);
    }

    return fib_arr[n - 1];
}


int main(){
   int test[44];
   int k = 5;
   test[k] = 44;
   test[k + 1] = 4;
   test[k - 1] = test[k] - test[k + 1];

   return fibb();

}