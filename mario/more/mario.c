#include <cs50.h>
#include <stdio.h>

int main(void)
{
   int height;
   int c = 0;

   do{
       printf("Welche Hoehe?\n");
       height = get_int();
   }while(height < 0 || height >= 24);

   for(int rows = height; rows > 0; rows--)
   {
       for(int space = 0; space < rows - 1; space++)
       {
           printf(" ");
       }
       printf("#");
       c++;
       for (int sethashes = 0; sethashes < c - 1; sethashes++)
       {
           printf("#");
       }
       printf("  ");
       for (int sethashes = 0; sethashes < c; sethashes++)
       {
           printf("#");
       }
       printf("\n");
   }
   return 0;
}
