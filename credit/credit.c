#include <cs50.h>
#include <stdio.h>

int main (void)
{
    long long ccnumber, xadd, x2;
    int addsum, x2prod, sum;

    do{
        printf("Your credit card number, please:\n");
        ccnumber = GetLongLong();
    }
    while(ccnumber < 0);

    for(xadd = ccnumber, addsum = 0; xadd > 0; xadd /= 100)
    {
        addsum += xadd % 10;
    }

    for ( x2 = ccnumber / 10, x2prod = 0; x2 > 0; x2 /= 100 )
    {
        if ( 2 * (x2 % 10) > 9 )
        {
            x2prod += (2 * (x2 % 10)) / 10;
            x2prod += (2 * (x2 % 10)) % 10;
        }
        else
            x2prod += 2 * (x2 % 10);
    }

    sum = addsum + x2prod;

    if ( sum % 10 == 0 )
    {
        if ( (ccnumber >= 340000000000000 && ccnumber < 350000000000000) || (ccnumber >= 370000000000000 && ccnumber < 380000000000000) )
            printf("AMEX\n");
        else if ( ccnumber >= 5100000000000000 && ccnumber < 5600000000000000 )
            printf("MASTERCARD\n");
        else if ( (ccnumber >= 4000000000000 && ccnumber < 5000000000000) || (ccnumber >= 4000000000000000 && ccnumber < 5000000000000000) )
            printf("VISA\n");
        else
            printf("INVALID\n");
    }
    else
        printf("INVALID\n");

    return 0;
}
