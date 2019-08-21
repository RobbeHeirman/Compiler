
#include <stdio.h>

int main(){
    int k = 12;
    int *k_ptr = &k;

    char read[3];
    read[0] = '%';
    read[1] = 'i';
    read[2] = '\0';
    char* r_ptr = &read[0];

    scanf(r_ptr, k_ptr);
    return k;
}