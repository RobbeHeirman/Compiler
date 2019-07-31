// Regressive test all previous implemented features

//int a = 12;
//char q = 'b';
//
//
//int c (int a, char b, float c, char * d){
//
//        int e = a;
//        char f = 'k';
//        char z = q;S
//
//        return e;
//}
//
//
//int main(){
//
//    int p_1 = 44;
//    char p_2 = 'z';
//    float p_3 = 4.44;
//    char * p_4 = &p_2;
//
//    return c(p_1, p_2, p_3, p_4);
//}

int main(){

    int a = 44;
    int *b = &a;
    int *c  = b;
    int d = *c;
    return 50;
}