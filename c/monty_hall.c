#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define true 1
#define false 0
#define SWITCH_DOORS 1
#define ROUNDS 1000000000

//#define PRINTOUT = 1 //Define for printout of text

/* Seed the random with a random value the clock doesn't work because
 * it only gets updated once per second, and rand is called multiple hundreds
 * of times per second.
 */
static int get_rand()
{
    srand(rand());
    return rand();
}

static int choose_door_to_open(int one, int two)
{
    if( one || two )  //If either door actually has the prize
    {
        return (one) ? 2 : 1; //Open the other one
    }

    //If neither door has the prize, just return a random door.
    return get_rand() % 2 + 1;
}

int choose_door_to_switch(int opens, int chosen_door)
{
    if(opens == 1)
        return (chosen_door == 2) ? 3 : 2;

    if(opens == 2)
        return (chosen_door == 1) ? 3 : 1;

    //Opens must be 3, no need for that extra compairison.
    return (chosen_door == 1) ? 2 : 1;
}

int main(int argc, char *argv[])
{
    unsigned int wins = 0;
    unsigned int losses = 0;
    unsigned int i = 1;
    int door_one, door_two, door_three;

    /*Seed the random generator with the time*/
    srand(time(NULL));



    for (i = 1 ; i < ROUNDS + 1; i++)
    {
        //Set up doors
        door_one = false;
        door_two = false;
        door_three = false;

        int door_with_prize = get_rand() % 3 + 1;

        if (door_with_prize == 1)
        {
            door_one = true;
        }
        else
        {
            if (door_with_prize == 2)
                door_two = true;
            else
                door_three = true;
        }

        #ifdef PRINTOUT
        printf("Doors\n");
        printf("One: %i \n", door_one);
        printf("Two: %i\n", door_two);
        printf("Three: %i\n", door_three);
        #endif

        //Have the program randomly choose a start door
        unsigned int chosen_door = get_rand() % 3 + 1;

        #ifdef PRINTOUT
        printf("Chosen Door: %i\n", chosen_door);
        #endif

        //Have the program randomly choose which door to open.
        unsigned int opens;
        if( chosen_door == 1 )
        {
            opens = choose_door_to_open(door_two, door_three);
            opens = (opens == 1) ? 2 : 3;
        }
        else
        {
            if( chosen_door == 2 )
            {
                opens = choose_door_to_open(door_one, door_three);
                opens = (opens == 1) ? 1 : 3;
            }
            else  //Chosen door must be 3
            {
                opens = choose_door_to_open(door_one, door_two);
                opens = (opens == 1) ? 1 : 2;
            }
        }

        #ifdef PRINTOUT
        printf("Door Opened: %i\n", opens);
        #endif

        //Have the program switch doors
        if (SWITCH_DOORS == true)
        {
            chosen_door = choose_door_to_switch(opens, chosen_door);
            #ifdef PRINTOUT
            printf("Change door to: %i \n", chosen_door);
            #endif
        }

        //Increment the proper number so we can do stats at the end.
        if (chosen_door == door_with_prize)
        {
            #ifdef PRINTOUT
            printf( "Win\n" );
            #endif
            wins++;
        }
        else
        {
            #ifdef PRINTOUT
            printf ("Lose\n");
            #endif
            losses++;
        }

        #ifdef PRINTOUT
        printf("===End of round: %i ===\n", i);
        #endif
    }

    printf( "===RESULTS===\n" );
    printf( "Wins: %i\n", wins);
    printf( "%f %% \n",(wins / (ROUNDS * 1.0))*100);
    printf( "Losses: %i\n", losses);
    printf( "%f %% \n",(losses / (ROUNDS * 1.0))*100);

    return 0;
}
