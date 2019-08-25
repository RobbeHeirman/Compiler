#include <stdio.h>
int pow(int a, int b){


        if (b == 0){

            return 1;
        }


    for(int i = 0; i < b - 1; i = i + 1){


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
    int pw = pow(2, 5);
    printf(r_ptr, pw);
    return pw;
}