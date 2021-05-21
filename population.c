#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start;

    do
    {
        start = get_int("Enter the starting amount of llamas (must be 9 or more): ");
     }
    while (start < 9);

    // TODO: Prompt for end size
    int result;

    do
    {
        result = get_int("Enter the resulting amount of llamas (must not be less than starting amount): ");
     }
    while (result < start);

    // TODO: Calculate number of years until we reach threshold
    int n = start, count = 0;

    do
    {
        n += n / 3 - n / 4;
        count += 1;
     }
    while (n < result);

    // TODO: Print number of years
    printf("Years: %i\n", count);
}