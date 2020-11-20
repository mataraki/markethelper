#include <cs50.h>
#include <stdio.h>
#include <string.h>

float getgrade(string text);

int main(void)
{
    string text = get_string("Enter the text: ");
    float grade = getgrade(text);
    
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    
    else
    {
        printf("Grade %.0f\n", grade);
    }
}

float getgrade(string text)
{
    int letters = 0;
    int words = 1;
    int sentences = 0;
    
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] == '.') && (text[i - 1] != '.'))
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
    float grade = 0.0588 * letters * 100 / words - 0.296 * sentences * 100 / words - 15.8;
    return grade;
}