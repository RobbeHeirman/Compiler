int main(){

    int a = 1;
    int b;
    b = a;

    char c = '1';
    char d;
    d = c;

    float e = 4.44;
    float f;
    f = e;

    int * g = &a;
    int *h;
    h = g;

    *g = b;

    return a;

}