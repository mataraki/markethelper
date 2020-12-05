#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }
        //for (int j = 0; j < candidate_count; j++)
        //{
        //    printf("%i\n", ranks[j]);
        //}
    
        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[i] = rank;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (ranks[i] < ranks[j])
            {
                preferences[i][j] += 1;
                preferences[j][i] -= 1;
            }
            else
            {
                preferences[i][j] -= 1;
                preferences[j][i] += 1;
            }
        }
    }
//    for (int i = 0; i < candidate_count; i++)
//    {
//        for (int j = i + 1; j < candidate_count; j++)
//        {
//            printf("%i", preferences[i][j]);
//        }
//    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    int k = 1;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] == 0)
            {
                k += 1;
            }
            else if (preferences[i][j] > 0)
            {
                pairs[i + j - k].winner = i;
                pairs[i + j - k].loser = j;
                pair_count += 1;
            }
            else
            {
                pairs[i + j - k].winner = j;
                pairs[i + j - k].loser = i;
                pair_count += 1;
            }
        }
    }
//    for (int i = 0; i < pair_count; i++)
//    {
//        printf("%i %i\n", pairs[i].winner, pairs[i].loser);
//    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int tempwinner = 0;
    int temploser = 0;
    for (int i = 0; i < pair_count; i++)
    {
        for (int j = i + 1; j < pair_count; j++)
        {
            preferences[i][j] = abs(preferences[i][j]);
        }
    }
    for (int i = 0; i < pair_count; i++)
    {
        for (int j = i + 1; j < pair_count; j++)
        {
            if (preferences[pairs[i].winner][pairs[i].loser] < preferences[pairs[j].winner][pairs[j].loser])
            {
                tempwinner = pairs[i].winner;
                pairs[i].winner = pairs[j].winner;
                pairs[j].winner = tempwinner;
                temploser = pairs[i].loser;
                pairs[i].loser = pairs[j].loser;
                pairs[j].loser = temploser;
            }
        }
    }
//    for (int i = 0; i < pair_count; i++)
//    {
//        printf("%i %i\n", pairs[i].winner, pairs[i].loser);
//    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    locked[pairs[0].winner][pairs[0].loser] = true;
//    printf("%i, %i\n", pairs[0].winner, pairs[0].loser);
    int winnersum = pairs[0].winner;
    int losersum = pairs[0].loser;
    
    for (int i = 1; i < pair_count; i++)
    {
        if ((winnersum + pairs[i].winner) != (losersum + pairs[i].loser))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
            winnersum += pairs[i].winner;
            losersum += pairs[i].loser;
//            printf("%i, %i\n", pairs[i].winner, pairs[i].loser);
        }
    }
    
    return;
}

// Print the winner of the election
void print_winner(void)
{
    int winner = pairs[0].winner;
    for (int i = 1; i < pair_count; i++)
    {
        if (locked[pairs[i].winner][pairs[i].loser] == true)
        {
            if (winner == pairs[i].loser)
            {
                winner = pairs[i].winner;
            }
        }
    }
    printf("%s", candidates[winner]);
    printf("\n");
    return;
}

