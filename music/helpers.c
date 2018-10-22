// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int x = atoi(&fraction[0]);
    int y = atoi(&fraction[2]);
    int duration = (8/y) * x;

    return duration;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    int octave = note[strlen(note) - 1];
    octave -= 48;

    double f = 0.0;

    switch(note[0])
    {
        case 'C':
            f = 440.0 / (pow(2.0, (9.0/12.0)));
            break;
        case 'D':
            f = 440.0 / (pow(2.0, (7.0/12.0)));
            break;
        case 'E':
            f = 440.0 / (pow(2.0, (5.0/12.0)));
            break;
        case 'F':
            f = 440.0 / (pow(2.0, (4.0/12.0)));
            break;
        case 'G':
            f = 440.0 / (pow(2.0, (2.0/12.0)));
            break;
        case 'A':
            f = 440.0;
            break;
        case 'B':
            f = 440.0 * (pow(2.0, (2.0/12.0)));
            break;
        default:
            return 0;
    }

    if(octave > 4)
    {
        for(int i = 0; i < octave - 4; i++)
        {
            f *= 2.0;
        }
    }else if(octave < 4)
    {
        for(int i = 0; i < 4 - octave; i++)
        {
            f /= 2.0;
        }
    }

    if(note[1] == 'b')
    {
        f /= pow(2.0, (1.0/12.0));
    }else if(note[1] == '#')
    {
        f *= pow(2.0, (1.0/12.0));
    }

    return round(f);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if(strcmp(s,"") == 0)
    {
        return true;
    }else
    {
        return false;
    }
}
