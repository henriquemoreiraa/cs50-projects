#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long card_number;

    do
    {
        card_number = get_long("Card number: ");
    }
    while (card_number < 1);

    int first_last_digit = 0;
    int second_last_digit = 0;
    int count_length = 0;
    long two_first_digits = card_number;
    int result;

    while (card_number)
    {
        // Calculate to get next second last digit
        int a = ((card_number / 10) % 10) * 2;
        // Calculate to get next first last digit
        int b = card_number % 10;

        // Verify second last digit to get two separate digits from it
        if (a > 9)
        {
            second_last_digit = (second_last_digit + 1) + (a % 10);
        }
        else
        {
            second_last_digit += a;
        }

        // Verify first last digit to get two separate digits from it
        if (b > 9)
        {
            first_last_digit = (first_last_digit + 1) + (b % 10);
        }
        else
        {
            first_last_digit += b;
        }

        // Decrease length of card number
        card_number = (card_number / 10) / 10;
        count_length++;
    }

    while (two_first_digits > 99)
    {
        // Get two first digists from credit card number
        two_first_digits = (two_first_digits / 10);
    }

    result = (second_last_digit + first_last_digit) % 10;
    count_length *= 2;

    if (result != 0 || count_length < 13 || count_length > 16)
    {
        printf("INVALID\n");
    }
    else if (two_first_digits == 34 || two_first_digits == 37)
    {
        printf("AMEX\n");
    }
    else if (two_first_digits > 50 && two_first_digits < 56)
    {
        printf("MASTERCARD\n");
    }
    else if (((int) two_first_digits / 10) == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}