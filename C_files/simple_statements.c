// Regressive test all previous implemented features

int a(int a){

return 12;
}
int main(){

    int a = 44;
    int *b = &a;
    int *c  = b;
    int d = *c;
    return d;
}