#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long number = get_long("Number: ");
    long number2 = number;
    while (number2 > 100)
    {
        number2 = number2 / 10;
    }
    int luhn = 0;
    int i = 1;
    while (number)
    {
        if (i % 2 == 1)
        {
            luhn += number % 10;
            number = number / 10;
        }
        else
        {
            luhn += ((number % 10) * 2) / 10;
            luhn += ((number % 10) * 2) % 10;
            number = number / 10;
        }
        i++;
    }
    if (luhn % 10 == 0)
    {
        if (number2 == 34 || number2 == 37)    
        {
            printf("AMEX\n");
        }
        else if (number2 > 50 && number2 < 56)
        {
            printf("MASTERCARD\n");
        }
        else if (number2 / 10 == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
        {
            printf("INVALID\n");
        }
}