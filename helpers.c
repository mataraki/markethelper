#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg = (int) round(((double) image[i][j].rgbtRed + (double) image[i][j].rgbtGreen + (double) image[i][j].rgbtBlue) / 3);
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j <= width / 2; j++)
        {
            int tempred = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][width-j+1].rgbtRed;
            image[i][width-j+1].rgbtRed = tempred;
            int tempblue = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][width-j+1].rgbtBlue;
            image[i][width-j+1].rgbtBlue = tempblue;
            int tempgreen = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][width-j+1].rgbtGreen;
            image[i][width-j+1].rgbtGreen = tempgreen;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
