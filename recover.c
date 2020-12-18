#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>  

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover file\n");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open %s\n", argv[1]);
        return 1;
    }
    
    unsigned char buffer[512];
    
    int filecount = 0;
    
    FILE *picture = NULL; 
    
    bool jpg_found = 0;
    
    while (fread(buffer, 512, 1, file) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
        {
            if (jpg_found)
            {
                fclose(picture);
            }
            else
            {
                jpg_found = 1;
            }

            
            char filename[8];
            sprintf(filename, "%03d.jpg", filecount);
            picture = fopen(filename, "a");
            filecount++;
        }
        
        if (jpg_found == 1)
        {
            fwrite(&buffer, 512, 1, picture);
        }
        
    }
    fclose(file);
    fclose(picture);

    return 0;
}
