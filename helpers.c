#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg = (int) round((double) (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3);
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
        for (int j = 0; j < width / 2; j++)
        {
            int tempred = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][width-j-1].rgbtRed;
            image[i][width-j-1].rgbtRed = tempred;
            int tempblue = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][width-j-1].rgbtBlue;
            image[i][width-j-1].rgbtBlue = tempblue;
            int tempgreen = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][width-j-1].rgbtGreen;
            image[i][width-j-1].rgbtGreen = tempgreen;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    const int a = height - 1;
    const int b = width - 1;
    RGBTRIPLE tempimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avgred;
            int avgblue;
            int avggreen;
            if (i == 0)
            {
                if (j == 0)
                {
                    avgred = (int) round((double) (image[i][j].rgbtRed + image[i][j+1].rgbtRed + image[i+1][j].rgbtRed + image[i+1][j+1].rgbtRed) / 4);
                    avgblue = (int) round((double) (image[i][j].rgbtBlue + image[i][j+1].rgbtBlue + image[i+1][j].rgbtBlue + image[i+1][j+1].rgbtBlue)/ 4);
                    avggreen = (int) round((double) (image[i][j].rgbtGreen + image[i][j+1].rgbtGreen + image[i+1][j].rgbtGreen + image[i+1][j+1].rgbtGreen)/ 4);
                }
                else if (j == width - 1)
                {
                    avgred = (int) round((double) (image[i][j-1].rgbtRed + image[i][j].rgbtRed + image[i+1][j-1].rgbtRed + image[i+1][j].rgbtRed) / 4);
                    avgblue = (int) round((double) (image[i][j-1].rgbtBlue + image[i][j].rgbtBlue + image[i+1][j-1].rgbtBlue + image[i+1][j].rgbtBlue)/ 4);
                    avggreen = (int) round((double) (image[i][j-1].rgbtGreen + image[i][j].rgbtGreen + image[i+1][j-1].rgbtGreen + image[i+1][j].rgbtGreen)/ 4);
                }
                else
                {
                    avgred = (int) round((double) (image[i][j-1].rgbtRed + image[i][j].rgbtRed + image[i][j+1].rgbtRed + image[i+1][j-1].rgbtRed + image[i+1][j].rgbtRed + image[i+1][j+1].rgbtRed) / 6);
                    avgblue = (int) round((double) (image[i][j-1].rgbtBlue + image[i][j].rgbtBlue + image[i][j+1].rgbtBlue + image[i+1][j-1].rgbtBlue + image[i+1][j].rgbtBlue + image[i+1][j+1].rgbtBlue)/ 6);
                    avggreen = (int) round((double) (image[i][j-1].rgbtGreen + image[i][j].rgbtGreen + image[i][j+1].rgbtGreen + image[i+1][j-1].rgbtGreen + image[i+1][j].rgbtGreen + image[i+1][j+1].rgbtGreen)/ 6);
                }
            }
            else if (i == height - 1)
            {
                if (j == 0)
                {
                    avgred = (int) round((double) (image[i-1][j].rgbtRed + image[i-1][j+1].rgbtRed + image[i][j].rgbtRed + image[i][j+1].rgbtRed) / 4);
                    avgblue = (int) round((double) (image[i-1][j].rgbtBlue + image[i-1][j+1].rgbtBlue + image[i][j].rgbtBlue + image[i][j+1].rgbtBlue)/ 4);
                    avggreen = (int) round((double) (image[i-1][j].rgbtGreen + image[i-1][j+1].rgbtGreen + image[i][j].rgbtGreen + image[i][j+1].rgbtGreen)/ 4);
                }
                else if (j == width - 1)
                {
                    avgred = (int) round((double) (image[i-1][j-1].rgbtRed + image[i-1][j].rgbtRed + image[i][j-1].rgbtRed + image[i][j].rgbtRed) / 4);
                    avgblue = (int) round((double) (image[i-1][j-1].rgbtBlue + image[i-1][j].rgbtBlue + image[i][j-1].rgbtBlue + image[i][j].rgbtBlue)/ 4);
                    avggreen = (int) round((double) (image[i-1][j-1].rgbtGreen + image[i-1][j].rgbtGreen + image[i][j-1].rgbtGreen + image[i][j].rgbtGreen)/ 4);
                }
                else
                {
                    avgred = (int) round((double) (image[i-1][j-1].rgbtRed + image[i-1][j].rgbtRed + image[i-1][j+1].rgbtRed + image[i][j-1].rgbtRed + image[i][j].rgbtRed + image[i][j+1].rgbtRed) / 6);
                    avgblue = (int) round((double) (image[i-1][j-1].rgbtBlue + image[i-1][j].rgbtBlue + image[i-1][j+1].rgbtBlue + image[i][j-1].rgbtBlue + image[i][j].rgbtBlue + image[i][j+1].rgbtBlue)/ 6);
                    avggreen = (int) round((double) (image[i-1][j-1].rgbtGreen + image[i-1][j].rgbtGreen + image[i-1][j+1].rgbtGreen + image[i][j-1].rgbtGreen + image[i][j].rgbtGreen + image[i][j+1].rgbtGreen)/ 6);
                }
            }
            else
            {
                if (j == 0)
                {
                    avgred = (int) round((double) (image[i-1][j].rgbtRed + image[i-1][j+1].rgbtRed + image[i][j].rgbtRed + image[i][j+1].rgbtRed + image[i+1][j].rgbtRed + image[i+1][j+1].rgbtRed) / 6);
                    avgblue = (int) round((double) (image[i-1][j].rgbtBlue + image[i-1][j+1].rgbtBlue + image[i][j].rgbtBlue + image[i][j+1].rgbtBlue + image[i+1][j].rgbtBlue + image[i+1][j+1].rgbtBlue)/ 6);
                    avggreen = (int) round((double) (image[i-1][j].rgbtGreen + image[i-1][j+1].rgbtGreen + image[i][j].rgbtGreen + image[i][j+1].rgbtGreen + image[i+1][j].rgbtGreen + image[i+1][j+1].rgbtGreen)/ 6);
                }
                else if (j == width - 1)
                {
                    avgred = (int) round((double) (image[i-1][j-1].rgbtRed + image[i-1][j].rgbtRed + image[i][j-1].rgbtRed + image[i][j].rgbtRed + image[i+1][j-1].rgbtRed + image[i+1][j].rgbtRed) / 6);
                    avgblue = (int) round((double) (image[i-1][j-1].rgbtBlue + image[i-1][j].rgbtBlue + image[i][j-1].rgbtBlue + image[i][j].rgbtBlue + image[i+1][j-1].rgbtBlue + image[i+1][j].rgbtBlue)/ 6);
                    avggreen = (int) round((double) (image[i-1][j-1].rgbtGreen + image[i-1][j].rgbtGreen + image[i][j-1].rgbtGreen + image[i][j].rgbtGreen + image[i+1][j-1].rgbtGreen + image[i+1][j].rgbtGreen)/ 6);
                }
                else
                {
                    avgred = (int) round((double) (image[i-1][j-1].rgbtRed + image[i-1][j].rgbtRed + image[i-1][j+1].rgbtRed + image[i][j-1].rgbtRed + image[i][j].rgbtRed + image[i][j+1].rgbtRed + image[i+1][j-1].rgbtRed + image[i+1][j].rgbtRed + image[i+1][j+1].rgbtRed) / 9);
                    avgblue = (int) round((double) (image[i-1][j-1].rgbtBlue + image[i-1][j].rgbtBlue + image[i-1][j+1].rgbtBlue + image[i][j-1].rgbtBlue + image[i][j].rgbtBlue + image[i][j+1].rgbtBlue + image[i+1][j-1].rgbtBlue + image[i+1][j].rgbtBlue + image[i+1][j+1].rgbtBlue) / 9);
                    avggreen = (int) round((double) (image[i-1][j-1].rgbtGreen + image[i-1][j].rgbtGreen + image[i-1][j+1].rgbtGreen + image[i][j-1].rgbtGreen + image[i][j].rgbtGreen + image[i][j+1].rgbtGreen + image[i+1][j-1].rgbtGreen + image[i+1][j].rgbtGreen + image[i+1][j+1].rgbtGreen) / 9);
                }
            }
            tempimage[i][j].rgbtRed = avgred;
            tempimage[i][j].rgbtBlue = avgblue;
            tempimage[i][j].rgbtGreen = avggreen;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = tempimage[i][j].rgbtRed;
            image[i][j].rgbtBlue = tempimage[i][j].rgbtBlue;
            image[i][j].rgbtGreen = tempimage[i][j].rgbtGreen;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
