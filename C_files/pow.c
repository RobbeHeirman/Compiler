#include <stdio.h>
int pow(int a, int b){


    for(int i = 0; i < b; i = i + 1){

        a = a + a;

    }

    return a;

}


int main(){

    char read[3];
    read[0] = '%';
    read[1] = 'i';
    read[2] = '\0';
    char* r_ptr = &read[0];
    int pw = pow(2, 4);
    printf(r_ptr, pw);
    return pw;
}