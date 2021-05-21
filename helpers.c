#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg = (int) round((double)(image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3);
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
            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;
            image[i][width - j - 1].rgbtRed = tempred;
            int tempblue = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;
            image[i][width - j - 1].rgbtBlue = tempblue;
            int tempgreen = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            image[i][width - j - 1].rgbtGreen = tempgreen;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
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
                    avgred = (int) round((double)(image[i][j].rgbtRed + image[i][j + 1].rgbtRed + 
                                                  image[i + 1][j].rgbtRed + image[i + 1][j + 1].rgbtRed) / 4);
                    avgblue = (int) round((double)(image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue + 
                                                   image[i + 1][j].rgbtBlue +  image[i + 1][j + 1].rgbtBlue) / 4);
                    avggreen = (int) round((double)(image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen + 
                                                    image[i + 1][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / 4);
                }
                else if (j == width - 1)
                {
                    avgred = (int) round((double)(image[i][j - 1].rgbtRed + image[i][j].rgbtRed + 
                                                  image[i + 1][j - 1].rgbtRed + image[i + 1][j].rgbtRed) / 4);
                    avgblue = (int) round((double)(image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue + 
                                                   image[i + 1][j - 1].rgbtBlue + image[i + 1][j].rgbtBlue) / 4);
                    avggreen = (int) round((double)(image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen + 
                                                    image[i + 1][j - 1].rgbtGreen + image[i + 1][j].rgbtGreen) / 4);
                }
                else
                {
                    avgred = (int) round((double)(image[i][j - 1].rgbtRed + image[i][j].rgbtRed + image[i][j + 1].rgbtRed + 
                                                  image[i + 1][j - 1].rgbtRed + image[i + 1][j].rgbtRed + image[i + 1][j + 1].rgbtRed) / 6);
                    avgblue = (int) round((double)(image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue + 
                                                   image[i + 1][j - 1].rgbtBlue + image[i + 1][j].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / 6);
                    avggreen = (int) round((double)(image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen + 
                                                    image[i + 1][j - 1].rgbtGreen + image[i + 1][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / 6);
                }
            }
            else if (i == height - 1)
            {
                if (j == 0)
                {
                    avgred = (int) round((double)(image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed + 
                                                  image[i][j].rgbtRed + image[i][j + 1].rgbtRed) / 4);
                    avgblue = (int) round((double)(image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue + 
                                                   image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue) / 4);
                    avggreen = (int) round((double)(image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen + 
                                                    image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen) / 4);
                }
                else if (j == width - 1)
                {
                    avgred = (int) round((double)(image[i - 1][j - 1].rgbtRed + image[i - 1][j].rgbtRed + 
                                                  image[i][j - 1].rgbtRed + image[i][j].rgbtRed) / 4);
                    avgblue = (int) round((double)(image[i - 1][j - 1].rgbtBlue + image[i - 1][j].rgbtBlue + 
                                                   image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue) / 4);
                    avggreen = (int) round((double)(image[i - 1][j - 1].rgbtGreen + image[i - 1][j].rgbtGreen + 
                                                    image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen) / 4);
                }
                else
                {
                    avgred = (int) round((double)(image[i - 1][j - 1].rgbtRed + image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed + 
                                                  image[i][j - 1].rgbtRed + image[i][j].rgbtRed + image[i][j + 1].rgbtRed) / 6);
                    avgblue = (int) round((double)(image[i - 1][j - 1].rgbtBlue + image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue + 
                                                   image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue) / 6);
                    avggreen = (int) round((double)(image[i - 1][j - 1].rgbtGreen + image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen + 
                                                    image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen) / 6);
                }
            }
            else
            {
                if (j == 0)
                {
                    avgred = (int) round((double)(image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed + image[i][j].rgbtRed + 
                                                  image[i][j + 1].rgbtRed + image[i + 1][j].rgbtRed + image[i + 1][j + 1].rgbtRed) / 6);
                    avgblue = (int) round((double)(image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue + image[i][j].rgbtBlue + 
                                                   image[i][j + 1].rgbtBlue + image[i + 1][j].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / 6);
                    avggreen = (int) round((double)(image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen + image[i][j].rgbtGreen + 
                                                    image[i][j + 1].rgbtGreen + image[i + 1][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / 6);
                }
                else if (j == width - 1)
                {
                    avgred = (int) round((double)(image[i - 1][j - 1].rgbtRed + image[i - 1][j].rgbtRed + image[i][j - 1].rgbtRed + 
                                                  image[i][j].rgbtRed + image[i + 1][j - 1].rgbtRed + image[i + 1][j].rgbtRed) / 6);
                    avgblue = (int) round((double)(image[i - 1][j - 1].rgbtBlue + image[i - 1][j].rgbtBlue + image[i][j - 1].rgbtBlue + 
                                                   image[i][j].rgbtBlue + image[i + 1][j - 1].rgbtBlue + image[i + 1][j].rgbtBlue) / 6);
                    avggreen = (int) round((double)(image[i - 1][j - 1].rgbtGreen + image[i - 1][j].rgbtGreen + image[i][j - 1].rgbtGreen + 
                                                    image[i][j].rgbtGreen + image[i + 1][j - 1].rgbtGreen + image[i + 1][j].rgbtGreen) / 6);
                }
                else
                {
                    avgred = (int) round((double)(image[i - 1][j - 1].rgbtRed + image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed + 
                                                  image[i][j - 1].rgbtRed + image[i][j].rgbtRed + image[i][j + 1].rgbtRed + 
                                                  image[i + 1][j - 1].rgbtRed + image[i + 1][j].rgbtRed + image[i + 1][j + 1].rgbtRed) / 9);
                    avgblue = (int) round((double)(image[i - 1][j - 1].rgbtBlue + image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue + 
                                                   image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue + 
                                                   image[i + 1][j - 1].rgbtBlue + image[i + 1][j].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / 9);
                    avggreen = (int) round((double)(image[i - 1][j - 1].rgbtGreen + image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen + 
                                                    image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen + 
                                                    image[i + 1][j - 1].rgbtGreen + image[i + 1][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / 9);
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
    RGBTRIPLE tempimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int Gxred;
            int Gyred;
            int Gxblue;
            int Gyblue;
            int Gxgreen;
            int Gygreen;
            if (i == 0)
            {
                if (j == 0)
                {
                    Gxred = (int) round((double)(image[i][j + 1].rgbtRed * 2 + image[i + 1][j + 1].rgbtRed * 1));
                    Gyred = (int) round((double)(image[i + 1][j].rgbtRed * 2 + image[i + 1][j + 1].rgbtRed * 1));
                    Gxblue = (int) round((double)(image[i][j + 1].rgbtBlue * 2 + image[i + 1][j + 1].rgbtBlue * 1));
                    Gyblue = (int) round((double)(image[i + 1][j].rgbtBlue * 2 + image[i + 1][j + 1].rgbtBlue * 1));
                    Gxgreen = (int) round((double)(image[i][j + 1].rgbtGreen * 2 + image[i + 1][j + 1].rgbtGreen * 1));
                    Gygreen = (int) round((double)(image[i + 1][j].rgbtGreen * 2 + image[i + 1][j + 1].rgbtGreen * 1));
                }
                else if (j == width - 1)
                {
                    Gxred = (int) round((double)(image[i][j - 1].rgbtRed * (-2) + image[i + 1][j - 1].rgbtRed * (-1)));
                    Gyred = (int) round((double)(image[i + 1][j - 1].rgbtRed * 1 + image[i + 1][j].rgbtRed * 2));
                    Gxblue = (int) round((double)(image[i][j - 1].rgbtBlue * (-2) + image[i + 1][j - 1].rgbtBlue * (-1)));
                    Gyblue = (int) round((double)(image[i + 1][j - 1].rgbtBlue * 1 + image[i + 1][j].rgbtBlue * 2));
                    Gxgreen = (int) round((double)(image[i][j - 1].rgbtGreen * (-2) + image[i + 1][j - 1].rgbtGreen * (-1)));
                    Gygreen = (int) round((double)(image[i + 1][j - 1].rgbtGreen * 1 + image[i + 1][j].rgbtGreen * 2));
                }
                else
                {
                    Gxred = (int) round((double)(image[i][j - 1].rgbtRed * (-2) + image[i + 1][j - 1].rgbtRed * (-1) +
                                                 image[i][j + 1].rgbtRed * 2 + image[i + 1][j + 1].rgbtRed * 1));
                    Gyred = (int) round((double)(image[i + 1][j - 1].rgbtRed * 1 + image[i + 1][j].rgbtRed * 2 +
                                                 image[i + 1][j + 1].rgbtRed * 1));
                    Gxblue = (int) round((double)(image[i][j - 1].rgbtBlue * (-2) + image[i + 1][j - 1].rgbtBlue * (-1) +
                                                  image[i][j + 1].rgbtBlue * 2 + image[i + 1][j + 1].rgbtBlue * 1));
                    Gyblue = (int) round((double)(image[i + 1][j - 1].rgbtBlue * 1 + image[i + 1][j].rgbtBlue * 2 +
                                                  image[i + 1][j + 1].rgbtBlue * 1));
                    Gxgreen = (int) round((double)(image[i][j - 1].rgbtGreen * (-2) + image[i + 1][j - 1].rgbtGreen * (-1) +
                                                   image[i][j + 1].rgbtGreen * 2 + image[i + 1][j + 1].rgbtGreen * 1));
                    Gygreen = (int) round((double)(image[i + 1][j - 1].rgbtGreen * 1 + image[i + 1][j].rgbtGreen * 2 +
                                                   image[i + 1][j + 1].rgbtGreen * 1));
                }
            }
            else if (i == height - 1)
            {
                if (j == 0)
                {
                    Gxred = (int) round((double)(image[i - 1][j + 1].rgbtRed * 1 + image[i][j + 1].rgbtRed * 2));
                    Gyred = (int) round((double)(image[i - 1][j].rgbtRed * (-2) + image[i - 1][j + 1].rgbtRed * (-1)));
                    Gxblue = (int) round((double)(image[i - 1][j + 1].rgbtBlue * 1 + image[i][j + 1].rgbtBlue * 2));
                    Gyblue = (int) round((double)(image[i - 1][j].rgbtBlue * (-2) + image[i - 1][j + 1].rgbtBlue * (-1)));
                    Gxgreen = (int) round((double)(image[i - 1][j + 1].rgbtGreen * 1 + image[i][j + 1].rgbtGreen * 2));
                    Gygreen = (int) round((double)(image[i - 1][j].rgbtGreen * (-2) + image[i - 1][j + 1].rgbtGreen * (-1)));
                }
                else if (j == width - 1)
                {
                    Gxred = (int) round((double)(image[i - 1][j - 1].rgbtRed * (-1) + image[i][j - 1].rgbtRed * (-2)));
                    Gyred = (int) round((double)(image[i - 1][j - 1].rgbtRed * (-1) + image[i - 1][j].rgbtRed * (-2)));
                    Gxblue = (int) round((double)(image[i - 1][j - 1].rgbtBlue * (-1) + image[i][j - 1].rgbtBlue * (-2)));
                    Gyblue = (int) round((double)(image[i - 1][j - 1].rgbtBlue * (-1) + image[i - 1][j].rgbtBlue * (-2)));
                    Gxgreen = (int) round((double)(image[i - 1][j - 1].rgbtGreen * (-1) + image[i][j - 1].rgbtGreen * (-2)));
                    Gygreen = (int) round((double)(image[i - 1][j - 1].rgbtGreen * (-1) + image[i - 1][j].rgbtGreen * (-2)));
                }
                else
                {
                    Gxred = (int) round((double)(image[i - 1][j + 1].rgbtRed * 1 + image[i][j + 1].rgbtRed * 2 +
                                                 image[i - 1][j - 1].rgbtRed * (-1) + image[i][j - 1].rgbtRed * (-2)));
                    Gyred = (int) round((double)(image[i - 1][j].rgbtRed * (-2) + image[i - 1][j + 1].rgbtRed * (-1) +
                                                 image[i - 1][j - 1].rgbtRed * (-1)));
                    Gxblue = (int) round((double)(image[i - 1][j + 1].rgbtBlue * 1 + image[i][j + 1].rgbtBlue * 2 +
                                                  image[i - 1][j - 1].rgbtBlue * (-1) + image[i][j - 1].rgbtBlue * (-2)));
                    Gyblue = (int) round((double)(image[i - 1][j].rgbtBlue * (-2) + image[i - 1][j + 1].rgbtBlue * (-1) +
                                                  image[i - 1][j - 1].rgbtBlue * (-1)));
                    Gxgreen = (int) round((double)(image[i - 1][j + 1].rgbtGreen * 1 + image[i][j + 1].rgbtGreen * 2 +
                                                   image[i - 1][j - 1].rgbtGreen * (-1) + image[i][j - 1].rgbtGreen * (-2)));
                    Gygreen = (int) round((double)(image[i - 1][j].rgbtGreen * (-2) + image[i - 1][j + 1].rgbtGreen * (-1) +
                                                   image[i - 1][j - 1].rgbtGreen * (-1)));
                }
            }
            else
            {
                if (j == 0)
                {
                    Gxred = (int) round((double)(image[i - 1][j + 1].rgbtRed * 1 + image[i][j + 1].rgbtRed * 2 +
                                                 image[i + 1][j + 1].rgbtRed * 1));
                    Gyred = (int) round((double)(image[i - 1][j].rgbtRed * (-2) + image[i - 1][j + 1].rgbtRed * (-1) +
                                                 image[i + 1][j].rgbtRed * 2 + image[i + 1][j + 1].rgbtRed * 1));
                    Gxblue = (int) round((double)(image[i - 1][j + 1].rgbtBlue * 1 + image[i][j + 1].rgbtBlue * 2 +
                                                  image[i + 1][j + 1].rgbtBlue * 1));
                    Gyblue = (int) round((double)(image[i - 1][j].rgbtBlue * (-2) + image[i - 1][j + 1].rgbtBlue * (-1) +
                                                  image[i + 1][j].rgbtBlue * 2 + image[i + 1][j + 1].rgbtBlue * 1));
                    Gxgreen = (int) round((double)(image[i - 1][j + 1].rgbtGreen * 1 + image[i][j + 1].rgbtGreen * 2 +
                                                   image[i + 1][j + 1].rgbtGreen * 1));
                    Gygreen = (int) round((double)(image[i - 1][j].rgbtGreen * (-2) + image[i - 1][j + 1].rgbtGreen * (-1) +
                                                   image[i + 1][j].rgbtGreen * 2 + image[i + 1][j + 1].rgbtGreen * 1));
                }
                else if (j == width - 1)
                {
                    Gxred = (int) round((double)(image[i - 1][j - 1].rgbtRed * (-1) + image[i][j - 1].rgbtRed * (-2) +
                                                 image[i + 1][j - 1].rgbtRed * (-1)));
                    Gyred = (int) round((double)(image[i - 1][j - 1].rgbtRed * (-1) + image[i - 1][j].rgbtRed * (-2) +
                                                 image[i + 1][j - 1].rgbtRed * 1 + image[i + 1][j].rgbtRed * 2));
                    Gxblue = (int) round((double)(image[i - 1][j - 1].rgbtBlue * (-1) + image[i][j - 1].rgbtBlue * (-2) +
                                                  image[i + 1][j - 1].rgbtBlue * (-1)));
                    Gyblue = (int) round((double)(image[i - 1][j - 1].rgbtBlue * (-1) + image[i - 1][j].rgbtBlue * (-2) +
                                                  image[i + 1][j - 1].rgbtBlue * 1 + image[i + 1][j].rgbtBlue * 2));
                    Gxgreen = (int) round((double)(image[i - 1][j - 1].rgbtGreen * (-1) + image[i][j - 1].rgbtGreen * (-2) +
                                                   image[i + 1][j - 1].rgbtGreen * (-1)));
                    Gygreen = (int) round((double)(image[i - 1][j - 1].rgbtGreen * (-1) + image[i - 1][j].rgbtGreen * (-2) +
                                                   image[i + 1][j - 1].rgbtGreen * 1 + image[i + 1][j].rgbtGreen * 2));
                }
                else
                {
                    Gxred = (int) round((double)(image[i - 1][j - 1].rgbtRed * (-1) + image[i][j - 1].rgbtRed * (-2) +
                                                 image[i + 1][j - 1].rgbtRed * (-1) + image[i - 1][j + 1].rgbtRed * 1 + 
                                                 image[i][j + 1].rgbtRed * 2 + image[i + 1][j + 1].rgbtRed * 1));
                    Gyred = (int) round((double)(image[i - 1][j].rgbtRed * (-2) + image[i - 1][j + 1].rgbtRed * (-1) +
                                                 image[i - 1][j - 1].rgbtRed * (-1) + image[i + 1][j - 1].rgbtRed * 1 + 
                                                 image[i + 1][j].rgbtRed * 2 + image[i + 1][j + 1].rgbtRed * 1));
                    Gxblue = (int) round((double)(image[i - 1][j - 1].rgbtBlue * (-1) + image[i][j - 1].rgbtBlue * (-2) +
                                                  image[i + 1][j - 1].rgbtBlue * (-1) + image[i - 1][j + 1].rgbtBlue * 1 + 
                                                  image[i][j + 1].rgbtBlue * 2 + image[i + 1][j + 1].rgbtBlue * 1));
                    Gyblue = (int) round((double)(image[i - 1][j].rgbtBlue * (-2) + image[i - 1][j + 1].rgbtBlue * (-1) +
                                                  image[i - 1][j - 1].rgbtBlue * (-1) + image[i + 1][j - 1].rgbtBlue * 1 + 
                                                  image[i + 1][j].rgbtBlue * 2 + image[i + 1][j + 1].rgbtBlue * 1));
                    Gxgreen = (int) round((double)(image[i - 1][j - 1].rgbtGreen * (-1) + image[i][j - 1].rgbtGreen * (-2) + 
                                                   image[i + 1][j - 1].rgbtGreen * (-1) + image[i - 1][j + 1].rgbtGreen * 1 + 
                                                   image[i][j + 1].rgbtGreen * 2 + image[i + 1][j + 1].rgbtGreen * 1));
                    Gygreen = (int) round((double)(image[i - 1][j].rgbtGreen * (-2) + image[i - 1][j + 1].rgbtGreen * (-1) +
                                                   image[i - 1][j - 1].rgbtGreen * (-1) + image[i + 1][j - 1].rgbtGreen * 1 + 
                                                   image[i + 1][j].rgbtGreen * 2 + image[i + 1][j + 1].rgbtGreen * 1));
                }
            }
            if (Gxred > 255 || Gxred < -255)
            {
                Gxred = 255;
            }
            if (Gyred > 255 || Gyred < -255)
            {
                Gyred = 255;
            }
            if (Gxblue > 255 || Gxblue < -255)
            {
                Gxblue = 255;
            }
            if (Gyblue > 255 || Gyblue < -255)
            {
                Gyblue = 255;
            }
            if (Gxgreen > 255 || Gxgreen < -255)
            {
                Gxgreen = 255;
            }
            if (Gygreen > 255 || Gygreen < -255)
            {
                Gygreen = 255;
            }
            double red = round(sqrt(pow((double)Gxred, 2) + pow((double)Gyred, 2)));
            if (red > 255)
            {
                red = 255;
            }
            double blue = round(sqrt(pow((double)Gxblue, 2) + pow((double)Gyblue, 2)));
            if (blue > 255)
            {
                blue = 255;
            }
            double green = round(sqrt(pow((double)Gxgreen, 2) + pow((double)Gygreen, 2)));
            if (green > 255)
            {
                green = 255;
            }
            tempimage[i][j].rgbtRed = (int) red;
            tempimage[i][j].rgbtBlue = (int) blue;
            tempimage[i][j].rgbtGreen = (int) green;
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
