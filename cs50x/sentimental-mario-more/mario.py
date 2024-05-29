from cs50 import get_int

# TODO

while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

for i in range(height):
    for s in range(height, i + 1, -1):
        print(" ", end="")

    for r in range(i + 1):
        print("#", end="")

    print("  ", end="")

    for l in range(i + 1):
        print("#", end="")

    print()