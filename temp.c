#include <cs50.h>
#include <stdbool.h>
#include <string.h>
#include "dictionary.h"
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>

int main(void)
{
    string word = "zaa";
    printf("%i\n", word[0]);
    printf("%i\n", atoi(&word[0]));
}