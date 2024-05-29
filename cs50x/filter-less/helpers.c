#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE *r = &image[i][j].rgbtRed;
            BYTE *g = &image[i][j].rgbtGreen;
            BYTE *b = &image[i][j].rgbtBlue;

            int average = round((*r + *g + *b) / 3.0);

            *r = average;
            *g = average;
            *b = average;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE *b = &image[i][j].rgbtBlue;
            BYTE *r = &image[i][j].rgbtRed;
            BYTE *g = &image[i][j].rgbtGreen;

            int sepiaRed = round((.393 * *r) + (.769 * *g) + (.189 * *b));
            int sepiaGreen = round((.349 * *r) + (.686 * *g) + (.168 * *b));
            int sepiaBlue = round((.272 * *r) + (.534 * *g) + (.131 * *b));

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            *b = sepiaBlue;
            *r = sepiaRed;
            *g = sepiaGreen;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            BYTE r_left = image[i][j].rgbtRed;
            BYTE g_left = image[i][j].rgbtGreen;
            BYTE b_left = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][width - (j + 1)].rgbtRed;
            image[i][width - (j + 1)].rgbtRed = r_left;

            image[i][j].rgbtGreen = image[i][width - (j + 1)].rgbtGreen;
            image[i][width - (j + 1)].rgbtGreen = g_left;

            image[i][j].rgbtBlue = image[i][width - (j + 1)].rgbtBlue;
            image[i][width - (j + 1)].rgbtBlue = b_left;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    int r_s = 0;
    int g_s = 0;
    int b_s = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int r_sum = 0;
            int g_sum = 0;
            int b_sum = 0;

            int count = 0;

            if (j + 1 < width)
            {
                r_sum += temp[i][j + 1].rgbtRed;
                g_sum += temp[i][j + 1].rgbtGreen;
                b_sum += temp[i][j + 1].rgbtBlue;
                count++;
            }
            if (j - 1 > 0)
            {
                r_sum += temp[i][j - 1].rgbtRed;
                g_sum += temp[i][j - 1].rgbtGreen;
                b_sum += temp[i][j - 1].rgbtBlue;
                count++;

            }
            if (i + 1 < height)
            {
                r_sum += temp[i + 1][j].rgbtRed;
                g_sum += temp[i + 1][j].rgbtGreen;
                b_sum += temp[i + 1][j].rgbtBlue;
                count++;

            }
            if (i - 1 > 0)
            {
                r_sum += temp[i - 1][j].rgbtRed;
                g_sum += temp[i - 1][j].rgbtGreen;
                b_sum += temp[i - 1][j].rgbtBlue;
                count++;

            }
            if (j + 1 < width && i + 1 < height)
            {
                r_sum += temp[i + 1][j + 1].rgbtRed;
                g_sum += temp[i + 1][j + 1].rgbtGreen;
                b_sum += temp[i + 1][j + 1].rgbtBlue;
                count++;

            }
            if (j - 1 > 0 && i - 1 > 0)
            {
                r_sum += temp[i - 1][j - 1].rgbtRed;
                g_sum += temp[i - 1][j - 1].rgbtGreen;
                b_sum += temp[i - 1][j - 1].rgbtBlue;
                count++;

            }
            if (j - 1 > 0 && i + 1 < width)
            {
                r_sum += temp[i + 1][j - 1].rgbtRed;
                g_sum += temp[i + 1][j - 1].rgbtGreen;
                b_sum += temp[i + 1][j - 1].rgbtBlue;
                count++;

            }
            if (j + 1 < width && i - 1 > 0)
            {
                r_sum += temp[i - 1][j + 1].rgbtRed;
                g_sum += temp[i - 1][j + 1].rgbtGreen;
                b_sum += temp[i - 1][j + 1].rgbtBlue;
                count++;
            }

            image[i][j].rgbtRed = round(r_sum / count);
            image[i][j].rgbtGreen = round(g_sum / count);
            image[i][j].rgbtBlue = round(b_sum / count);
        }
    }

    return;
}
