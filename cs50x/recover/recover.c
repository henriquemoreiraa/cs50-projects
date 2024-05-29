#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint8_t  BYTE;

int const BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // Check if is the correct usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    // Open file received from argv
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    int img_count = 0;
    BYTE file[BLOCK_SIZE];
    FILE *img;

    // Loop until fread returns full block
    while (fread(&file, 1, BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        // Check if first 4 bytes are the start of jpeg file
        if (file[0] == 0xff && file[1] == 0xd8 && file[2] == 0xff && (file[3] & 0xf0) == 0xe0)
        {
            if (img_count > 0)
            {
                fclose(img);
            }

            char *filename = malloc(8);
            sprintf(filename, "%03i.jpg", img_count);

            img = fopen(filename, "w");
            fwrite(file, 1, BLOCK_SIZE, img);

            img_count++;
            free(filename);
        }
        else
        {
            if (img_count > 0)
            {
                // Write block on image
                fwrite(&file[0], 1, BLOCK_SIZE, img);
            }
        }
    }

    fclose(img);
    fclose(card);
}