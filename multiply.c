#include <stdio.h>
#include <stdlib.h>

int multiply(long a, long b){
    return a*b;
}

int main(){
    for(long i=1 ; i<= 10000000 ; i++){
        long a = rand()%10000 + 10000000;
        long b = rand()%10000 + 10000000;
        long result = multiply(a,b);
        }
    return 0;
}

