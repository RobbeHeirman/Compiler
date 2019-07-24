
int a(int* b){
    return *b;
}

int main(){
    int d = 456;
    int *e = &d;
    int b = a(e);
    return b;
}