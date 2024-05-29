#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    do
    {
        height = get_int("Height of pyramid: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        // Add space at right
        for (int b = height; b > i + 1; b--)
        {
            printf(" ");
        }

        // Add right side of pyramid
        for (int a = 0; a <= i; a++)
        {
            printf("#");
        }
        printf("  ");

        // Add left side of pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}