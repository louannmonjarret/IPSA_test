#include <stdio.h>
#include "function_def.h"

void hello_world() {
    printf("Hello world!\n");
}

int compare(int a,int b)
{
	if(a>b){
		printf(" %d est plus grand que %d", a,b); //premier %d remplacé par a 
	}
	if(a==b){
		printf(" les nombres sont égaux");
	}
	else {
		printf(" %d est plus grand que %d", b,a);
	}
}

void loop_1_100()
{
	for( int i=1 ; i < 101 ; i++){
		printf("%d \n",i);
	}
}

void while_1_100()
{
	int i = 1;
	while( i <= 100){
		printf("%d \n",i);
		i++;	
	}
}

void assign(int x)
{
	printf("La valeur de la variable est : %d \n",x);// %d c'est dans le cas d'un entier
	printf("Son adresse mémoire est : %p \n", &x); // %p c'est pour dire qu'on affiche la valeur après (&x) et p c'est dans le cas d'un pointeur
}

int sum(int a, int b)
{
	return a+b;
}
