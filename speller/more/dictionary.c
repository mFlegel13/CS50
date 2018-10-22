// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "dictionary.h"

#define SIZE 1000000

typedef struct node
{
    char word[LENGTH+1];
    struct node* next;
}
node;

node* hashtable[SIZE] = {NULL};

int hash (const char* word)
{
    int hash = 0;
    int n;
    for (int i = 0; word[i] != '\0'; i++)
    {
        if(isalpha(word[i]))
        {
            n = word [i] - 'a' + 1;
        }else
        {
            n = 27;
        }
        hash = ((hash << 3) + n) % SIZE;
    }
    return hash;
}
int dictionarySize = 0;

//Loads dictionary into memory.  Returns true if successful else false.
bool load(const char* dictionary)
{
    FILE* file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    char word[LENGTH+1];

    while (fscanf(file, "%s\n", word)!= EOF)
    {
        dictionarySize++;

        node* newWord = malloc(sizeof(node));
        strcpy(newWord->word, word);
        int index = hash(word);

        if (hashtable[index] == NULL)
        {
            hashtable[index] = newWord;
            newWord->next = NULL;
        }else
        {
            newWord->next = hashtable[index];
            hashtable[index] = newWord;
        }
    }
    fclose(file);
    return true;
}

//Returns true if word is in dictionary else false.
bool check(const char* word)
{
    char temp[LENGTH+1];
    int len = strlen(word);

    for(int i = 0; i < len; i++)
    {
        temp[i] = tolower(word[i]);
    }
    temp[len] = '\0';

    int index = hash(temp);

    if(hashtable[index] == NULL)
    {
        return false;
    }

    node* cursor = hashtable[index];

    while(cursor != NULL)
    {
        if(strcmp(temp, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if(dictionarySize > 0)
    {
        return dictionarySize;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    int index = 0;

    while(index < SIZE)
    {
        if(hashtable[index] == 0)
        {
            index++;
        }else
        {
            while(hashtable[index] != 0)
            {
                node* cursor = hashtable[index];
                hashtable[index] = cursor->next;
                free(cursor);
            }
            index++;
        }
    }

    return true;
}
