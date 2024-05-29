from cs50 import get_int

# TODO
while True:
    card_number = get_int("Number: ")
    if card_number > 0:
        break

first_last_digit = 0
second_last_digit = 0
count_length = 0
two_first_digits = card_number
result = 0

while int(card_number) != 0:
    a = int((abs(card_number / 10) % 10)) * 2
    b = int(abs(card_number) % 10)

    if a > 9:
        second_last_digit = (second_last_digit + 1) + int((abs(a) % 10))
    else:
        second_last_digit += a

    if b > 9:
        first_last_digit = (first_last_digit + 1) + int((abs(b) % 10))
    else:
        first_last_digit += b

    card_number = (int(card_number) / 10) / 10
    count_length += 1

while (two_first_digits > 99):
    two_first_digits = (two_first_digits / 10)

result = (int(second_last_digit) + int(first_last_digit)) % 10
count_length *= 2

if (int(result) != 0 or count_length < 13 or count_length > 16):
    print("INVALID")
elif (int(two_first_digits) == 34 or int(two_first_digits) == 37):
    print("AMEX")
elif (int(two_first_digits) > 50 and int(two_first_digits) < 56):
    print("MASTERCARD")
elif (int((two_first_digits / 10)) == 4):
    print("VISA")
else:
    print("INVALID")
