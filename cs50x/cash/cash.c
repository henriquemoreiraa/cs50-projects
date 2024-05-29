#include <cs50.h>
#include <stdio.h>

int calculate_cents(int cents, int coin);
int get_cents(void);

int main(void)
{
    // Ask how many cents the customer is owed
    int cents = get_cents();

    // Calculate the number of quarters to give the customer
    int quarters = calculate_cents(cents, 25);
    cents = cents - quarters * 25;

    // Calculate the number of dimes to give the customer
    int dimes = calculate_cents(cents, 10);
    cents = cents - dimes * 10;

    // Calculate the number of nickels to give the customer
    int nickels = calculate_cents(cents, 5);
    cents = cents - nickels * 5;

    // Calculate the number of pennies to give the customer
    int pennies = calculate_cents(cents, 1);
    cents = cents - pennies * 1;

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;

    // Print total number of coins to give the customer
    printf("%i\n", coins);
}

int get_cents(void)
{
    int cents;

    do
    {
        cents = get_int("Cents: ");
    }
    while (cents < 1);

    return cents;
}

int calculate_cents(int cents, int coin)
{
    int count = 0;

    while (cents >= coin)
    {
        count++;
        cents -= coin;
    }

    return count;
}
