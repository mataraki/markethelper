// Implements a dictionary's functionality
#include <cs50.h>
#include <stdbool.h>
#include <string.h>
#include "dictionary.h"
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of words in the dictionary
int vocabulary = 0;

// Number of buckets in hash table
const unsigned int N = 677;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int position = hash(word);

    node *cursor = table[position];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO Hashes every word to it's index in the table
    int index;

    if (strlen(word) == 1)
    {
        index = 676;
    }
    else
    {
        index = (tolower(word[0]) - 97) * 26 + tolower(word[1]) - 97;
    }
    return index;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char *w = malloc(LENGTH);
    int position;

    for (int i = 0; i < 677; i++)
    {
        table[i] = malloc(sizeof(node));
    }

    FILE *file = fopen(dictionary, "r");

    if (file == NULL)
    {
        return false;
    }

    // TODO hash the words and insert them into table
    else while (fscanf(file, "%s", w) != EOF)
    {
        //Hash the word
        position = hash(w);
        vocabulary += 1;

        // Creates a node and sets it right
        node *n = malloc(sizeof(node));
        strcpy(n->word, w);
        n->next = table[position]->next;
        table[position]->next = n;
    }
    free(w);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return vocabulary;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < 677; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
