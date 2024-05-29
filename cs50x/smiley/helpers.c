#include "helpers.h"
#include <stdio.h>

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Change all black pixels to a color of your choosing

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Get memory addresses for the colors based on width and height
            BYTE *b = &image[i][j].rgbtBlue;
            BYTE *r = &image[i][j].rgbtRed;
            BYTE *g = &image[i][j].rgbtGreen;

            // Check if black color was found
            if (*b == 0)
            {
                // Change red color 0 to 255
                *r = 255;
                // Change green color 0 to 221
                *g = 221;
            }
        }
    }
}
