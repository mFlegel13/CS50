#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    int c = 0;

    if(argv[1] > 0 && argc == 2)
    {
        int inputKey = atoi(argv[1]);
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");

        for(int i=0;i<strlen(plaintext);i++)
        {
            if((plaintext[i] >= 'a' && plaintext[i] <= 'z') || (plaintext[i] >= 'A' && plaintext[i] <= 'Z') )
            {
                if(isupper(plaintext[i]))
                {
                    c = (plaintext[i] - 65 + inputKey) % 26;
                    c += 65;
                }else if(islower(plaintext[i]))
                {
                    c = (plaintext[i] - 97 + inputKey) % 26;
                    c += 97;
                }
                printf("%c", c);
            }else
            {
                printf("%c",plaintext[i]);
            }
        }
        printf("\n");
        return 0;
    }else
        printf("Usage: ./caesar key\n");
        return 1;
}