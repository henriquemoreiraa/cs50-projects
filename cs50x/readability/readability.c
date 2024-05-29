#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    int num_letters = 0;
    int num_words = 1;
    int num_sentences = 0;

    string text = get_string("Text: ");

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char current_char = text[i];

        if ((current_char > 64 && current_char < 91) || (current_char > 96 && current_char < 123))
        {
            num_letters++;
        }
        if (current_char == 32)
        {
            num_words++;
        }
        if (current_char == 46 || current_char == 33 || current_char == 63)
        {
            num_sentences++;
        }
    }

    double average_l = ((double) num_letters / (double) num_words) * 100;
    double average_s = ((double) num_sentences / (double) num_words) * 100;

    int result = round(0.0588 * average_l - 0.296 * average_s - 15.8);

    if (result < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (result >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", result);
    }
}