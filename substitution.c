#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string cipher(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    
    else if (strlen(argv[1]) != 26)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (argv[1][i] < 'A' || (argv[1][i] > 'Z' && argv[1][i] < 'a') || argv[1][i] > 'z')
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
        
        for (int j = i + 1; j < strlen(argv[1]); j++)
        {
            if (argv[1][j] == argv[1][i])
            {
                printf("Usage: ./substitution key\n");
                return 1;
            }
        }
    }
    
    string key = argv[1];
    
    string plaintext = get_string("plaintext: ");
    
    printf("ciphertext: %s", cipher(plaintext, key));
    printf("\n");
}

string cipher(string plaintext, string key)
{
    string ciphertext = plaintext;
    
    for (int i = 0; i < strlen(key); i++)
    {
        key[i] = toupper(key[i]);
    }
    
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if ((plaintext[i] >= 'A' && plaintext[i] <= 'Z') || (plaintext[i] >= 'a' && plaintext[i] <= 'z'))
        {
            if (plaintext[i] > 'Z')
            {
                int j = (int) plaintext[i] - 97;
                ciphertext[i] = tolower(key[j]);
            }
            
            else
            {
                int j = (int) plaintext[i] - 65;
                ciphertext[i] = key[j];
            }
        }
    }
    return ciphertext;
}