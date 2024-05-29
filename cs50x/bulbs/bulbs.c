#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    string message = get_string("Message: ");
    int message_length = strlen(message);
    int numbers[message_length][BITS_IN_BYTE];

    // Looping through the message to get char
    for (int i = 0, n = message_length; i < n; i++)
    {
        char current_char = message[i];
        int count = BITS_IN_BYTE - 1;

        // Looping until current_char reaches 0
        while (current_char > 0)
        {
            // Get bit
            int bit = current_char % 2;

            // Assigning one bit at the position of number in count
            numbers[i][count] = bit;

            // Divide by 2 to get next bit
            current_char /= 2;
            count--;

            // Checking if it is the last loop through current_char
            if (current_char < 1)
            {
                // Checking if needs to add two more zero at the start
                if (count == 1)
                {
                    numbers[i][count] = 0;
                    numbers[i][0] = 0;
                }
                // Add one zero at the start
                else
                {
                    numbers[i][count] = 0;
                }
            }
        }
    }

    // Looping through numbers array
    for (int i = 0; i < message_length; i++)
    {
        for (int j = 0; j < BITS_IN_BYTE; j++)
        {
            // Printing bulbs
            print_bulb(numbers[i][j]);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
