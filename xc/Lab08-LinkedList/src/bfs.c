/*
 * bfs.c
 *
 * A breadth first search algorithm
 *
 *  Created on: May 17, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */

#include <stdlib.h>
#include "bfs.h"
#include <assert.h>

// definitions
#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3

// declarations
struct list_t;
struct list_element_t_struct;
struct list_element_t_struct
{
	int rank ;
	struct list_element_t_struct* next ;
};


typedef struct list_element_t_struct  list_element_t;
typedef struct
{
	list_element_t* head;
	list_element_t* tail;
} list_t;



// prototypes
void push_back(list_t* list, int rank);
list_t init_list();
void free_list(list_t* list);
int remove_front(list_t* list);
void push_front(list_t* list, int rank);
void fill_neighbors(int neighbors[], int rank);


/** Functions **/

int test_main()
{
	// test init_list()
	list_t l1;
	l1 = init_list();
	assert(l1.head == l1.tail && l1.head == NULL);

	// test push_back;
	push_back(&l1, 10);
	assert(l1.head != NULL);
	assert(l1.tail == l1.head);
	assert(l1.head->rank == 10);
	assert(l1.head->next == NULL);

	push_back(&l1, 20);
	assert(l1.head != l1.tail);
	assert(l1.head->rank == 10);
	assert(l1.head->next == l1.tail);
	assert(l1.tail->rank == 20);
	assert(l1.tail->next == NULL);

	// test remove_front
	assert(remove_front(&l1) == 10);
	assert(l1.head != NULL);
	assert(l1.tail == l1.head);
	assert(l1.head->rank == 20);
	assert(l1.head->next == NULL);
	assert(remove_front(&l1) == 20);
	assert(l1.head == l1.tail && l1.head == NULL);

	// test free_list
	free_list(&l1);
	assert(l1.head == l1.tail && l1.head == NULL);

	// test push_front;
	push_front(&l1, 10);
	assert(l1.head != NULL);
	assert(l1.tail == l1.head);
	assert(l1.head->rank == 10);
	assert(l1.head->next == NULL);

	push_front(&l1, 20);
	assert(l1.head != l1.tail);
	assert(l1.head->rank == 20);
	assert(l1.head->next == l1.tail);
	assert(l1.tail->rank == 10);
	assert(l1.tail->next == NULL);

	// fill_neighbors
	int init[4];
	fill_neighbors(init, 0); // NW
	assert(init[NORTH] == -1);
	assert(init[EAST] != -1);
	assert(init[SOUTH] != -1);
	assert(init[WEST] == -1);

	return 0;
}



/**
This function should declare a new list t variable, ensure that both the head and tail ele-
ments are NULL, and return it.
**/
list_t init_list()
{
	list_t a;
	a.head = NULL;
	a.tail = NULL;

	return a;
}


void push_back(list_t* list, int rank)
{
	list_element_t* tmp = (list_element_t*) malloc (sizeof(list_element_t));
	assert(tmp != NULL); // if out of heap, we'll be null

	tmp->rank = rank;
	tmp->next = NULL;

	if(list->tail == NULL)
	{
		list->head = tmp;
		list->tail = tmp;
		return;
	}

	list->tail->next = tmp;
	list->tail = tmp;
}


void free_list(list_t* list)
{
	list_element_t* tmp = list->head;
	list_element_t* last;

	while(tmp != NULL)
	{
		last = tmp;
		tmp = tmp->next;

		free(last);
	}

	*list = init_list();
}


int remove_front(list_t* list)
{
	list_element_t* tmp = list->head;
	int val;

	if(tmp == NULL)
		return -1;

	val = tmp->rank;

	// fix up the head
	list->head = tmp->next;

	// fix up the tail (if needed)
	if(list->tail == tmp)
		*list = init_list();

	free(tmp);

	return val;
}

void push_front(list_t* list, int rank)
{
	list_element_t* tmp = (list_element_t*) malloc (sizeof(list_element_t));
	assert(tmp != NULL); // if out of heap, we'll be null

	tmp->rank = rank;
	tmp->next = list->head;

	list->head = tmp;


	if(list->tail == NULL)
		list->tail = tmp;
}




void fill_neighbors(int neighbors[], int rank)
{
	int row = ROW(rank);
	int col = COL(rank);

	// FILL NORTH
	if(row - 1 >= 0)
		neighbors[NORTH] = RANK(row - 1, col);
	else
		neighbors[NORTH] = -1;

	// FILL WEST
	if(col - 1 >= 0)
		neighbors[WEST] = RANK(row, col - 1);
	else
		neighbors[WEST] = -1;

	// FILL SOUTH
	if(row + 1 < MAZE_WIDTH)
		neighbors[SOUTH] = RANK(row + 1, col);
	else
		neighbors[SOUTH] = -1;

	// FILL EAST
	if(col + 1 < MAZE_WIDTH)
		neighbors[EAST] = RANK(row, col + 1);
	else
		neighbors[EAST] = -1;
}




