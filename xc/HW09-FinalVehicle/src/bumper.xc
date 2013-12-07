/*
 * bumpers.xc
 *
 *  Created on: May 28, 2012
 *      Author: joseph
 */

#include <xs1.h>
#include "platform.h"
#include "print.h"
#include "common_cmds.h"

in port leftbumper = XS1_PORT_1G;
in port rightbumper = XS1_PORT_1H;

void wait_left_bumper_press()
{
	leftbumper when pinseq(1) :> void;
}

void wait_right_bumper_press()
{
	rightbumper when pinseq(1) :> void;

}

void wait_either_bumper_press()
{
	select
	{
		case leftbumper when pinseq(1) :> void:
			break;

		case rightbumper when pinseq(1) :> void:
			break;
	}
}

void wait_left_bumper_release()
{
	leftbumper when pinseq(0) :> void;
}

void wait_right_bumper_release()
{
	rightbumper when pinseq(0) :> void;

}

void wait_all_bumper_release()
{
	leftbumper when pinseq(0) :> void;
	rightbumper when pinseq(0) :> void;
}

int left_is_hit()
{
	int j;
	leftbumper :> j;

	return j == 1;
}

int right_is_hit()
{
	int j;
	rightbumper :> j;

	return j == 1;
}

int bumper_is_hit()
{
	return (right_is_hit() || left_is_hit());
}

void test_bumpers()
{
	printstrln("==TESTING BUMPERS==");
	printstrln("Press Left bumper");
	wait_left_bumper_press();
	wait_left_bumper_release();

	printstrln("Press Right bumper");
	wait_right_bumper_press();
	wait_right_bumper_release();

	printstrln("Press either bumper 1/2");
	wait_either_bumper_press();
	wait_all_bumper_release();

	printstrln("Press either bumper 2/2");
	wait_either_bumper_press();
	wait_all_bumper_release();
	printstrln("==END TESTING BUMPERS==");

}
