// Regressive test all previous implemented features

#include <stdio.h>

int main(){

 char a[5];
 a[0] = 'h';
 a[1] = 'i';
 a[2] = '\r';
 a[3] = '\n';
 a[4] = '\0';
 char *b = &a[0];
 printf(b);

 return 40;
}