int gl_declared = 4012;

int a(int b){

    return b;
}

int b(int d){

    return d;

}

int c (int a, int b, char d){

    return a;
}


int main(){

    int first = a(88);

    int second = b(first);

    return c(second, gl_declared, 'a');

}