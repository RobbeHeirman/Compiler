int fibb(int n){

    if (n < 0){

        return 0;

    }

    else if (n == 0){

        return 1;
    }

    else if (n == 1){

        return 1;
    }

    return fibb(n -1) + fibb(n- 2);

}


int main(){

    return fibb(4);
}