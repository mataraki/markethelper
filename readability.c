#include <cs50.h>
#include <stdio.h>
#include <string.h>

float grade(string text);

int main(void)
{
    string text = get_string("Enter the text: ");
    printf("Grade %.0f\n", grade(text));
}

float grade(string text)
{
    int letters = 0;
    int words = 1;
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] == '.') && (text[i-1] != '.'))
        {
            sentences += 1;
        }
        else if (text[i] == '!')
        {
            sentences += 1;
        }
        else if (text[i] == '?')
        {
            sentences += 1;
        }
        else if (text[i] == ' ')
        {
            words += 1;
        }
        else if ((text[i] >= 'A' && text[i] <= 'Z') || (text[i] >= 'a' && text[i] <= 'z'))
        {
            letters += 1;
        }
    }
    //printf("%i %i %i\n", letters, words, sentences);
    float grade = 0.0588 * letters * 100 / words - 0.296 * sentences * 100 / words - 15.8;
    return grade;
}