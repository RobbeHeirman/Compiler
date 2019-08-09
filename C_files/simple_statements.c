



int fibbonaci(int n){

    if (n < 0){

        return 0;
    }

    else if ( n == 0){

        return 1;
    }

    else if (n == 1){

        return 1;
    }

    return fibbonaci(n -1) + fibbonaci(n - 2);
}


int main(){

    return fibbonaci(5);
}