#include <stdio.h>

int main(){
    char write[49];
    write[0] = 'W';
    write[1] = 'r';
    write[2] = 'i';
    write[3] = 't';
    write[4] = 'i';
    write[5] = 'n';
    write[6] = 'g';
    write[7] = ' ';
    write[8] = 'f';
    write[9] = 'i';
    write[10] = 'b';
    write[11] = 'o';
    write[12] = 'n';
    write[13] = 'a';
    write[14] = 'c';
    write[15] = 'c';
    write[16] = 'i';
    write[17] = ' ';
    write[18] = 's';
    write[19] = 'e';
    write[20] = 'q';
    write[21] = 'u';
    write[22] = 'e';
    write[23] = 'n';
    write[24] = 'c';
    write[25] = 'e';
    write[26] = ' ';
    write[27] = 'p';
    write[28] = 'l';
    write[29] = 'e';
    write[30] = 'a';
    write[31] = 's';
    write[32] = 'e';
    write[33] = ' ';
    write[34] = 'e';
    write[35] = 'n';
    write[36] = 't';
    write[37] = 'e';
    write[38] = 'r';
    write[39] = ' ';
    write[40] = 'a';
    write[41] = ' ';
    write[42] = 'd';
    write[43] = 'i';
    write[44] = 'g';
    write[45] = 'i';
    write[46] = 't';
    write[47] = '\n';
    write[48] = '\0';

    char * w_ptr = &write[0];
    printf(w_ptr);

    int k;
    int *k_ptr = &k;

    char read[3];
    read[0] = '%';
    read[1] = 'i';
    read[2] = '\0';
    char* r_ptr = &read[0];
    scanf(r_ptr, k_ptr);
    int fibb_arr[100];

    int n = 0;
    while(n < k){

        if (n == 0){
            fibb_arr[n] = 1;
        }

        else if (n == 1){
            fibb_arr[n] = 1;
        }

        else{

            fibb_arr[n] = fibb_arr[n -1] + fibb_arr[n - 2];
        }

        char write[4];
        write[0] = '%';
        write[1] = 'i';
        write[2] = ' ';
        write[3] = '\0';

        char* w = &write[0];
        printf(w, fibb_arr[n]);
        n = n + 1;

    }

    return fibb_arr[n - 1];
}