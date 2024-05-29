from cs50 import get_string

# TODO
num_letters = 0
num_words = 1
num_sentences = 0

text = get_string("Text: ")

for i in range(len(text)):
    current_char = text[i]

    if ((ord(current_char) > 64 and ord(current_char) < 91) or (ord(current_char) > 96 and ord(current_char) < 123)):
        num_letters += 1

    if (ord(current_char) == 32):
        num_words += 1

    if (ord(current_char) == 46 or ord(current_char) == 33 or ord(current_char) == 63):
        num_sentences += 1

average_l = (num_letters / num_words) * 100
average_s = (num_sentences / num_words) * 100

result = round((0.0588 * average_l) - (0.296 * average_s) - 15.8)

if (result < 1):
    print("Before Grade 1")
elif (result >= 16):
    print("Grade 16+")
else:
    print("Grade", result)
