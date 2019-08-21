
#include <stdio.h>

int fibb(){

    int fib_arr[50];
    int n = 10;
    int k = 0;
    while(k < n){

    if (k == 0){
        fib_arr[k] = 1;
    }

    else if (k == 1){

        fib_arr[k] = 1;
    }

    else{
       fib_arr[k] = fib_arr[k - 1] + fib_arr[k - 2];
    }

    k = k + 1;

    char print_arr[4];
    print_arr[0] = '%';
    print_arr[1] = 'i';
    print_arr[2] = ' ';
    print_arr[3] = '\0';

    char* print_ptr = &print_arr[0];
    printf(print_ptr, fib_arr[k - 1]);
    }

    char print_arr[2];
    print_arr[0] = '\n';
    print_arr[1] = '\0';
    char *ptr = &print_arr[0];
    printf(ptr);
    return fib_arr[n - 1];
}


int main(){
   return fibb();

}