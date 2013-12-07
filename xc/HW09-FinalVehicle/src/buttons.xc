/*
 * buttons.xc
 *
 *  Created on: May 28, 2012
 *      Author: joseph
 */

#include <xs1.h>
#include "platform.h"
#include "print.h"
#include "common_cmds.h"

in port leftButton = PORT_BUT_1;
in port rightButton = PORT_BUT_2;

void wait_left_button_press()
{
	leftButton when pinseq(0) :> void;
}

void wait_right_button_press()
{
	rightButton when pinseq(0) :> void;

}

void wait_either_button_press()
{
	select
	{
		case leftButton when pinseq(0) :> void:
			break;

		case rightButton when pinseq(0) :> void:
			break;
	}
}

void wait_left_button_release()
{
	leftButton when pinseq(1) :> void;
}

void wait_right_button_release()
{
	rightButton when pinseq(1) :> void;

}

void wait_all_button_release()
{
	leftButton when pinseq(1) :> void;
	rightButton when pinseq(1) :> void;
}


void test_buttons()
{
	printstrln("==TESTING BUTTONS==");
	printstrln("Press Left Button");
	wait_left_button_press();
	wait_left_button_release();

	printstrln("Press Right Button");
	wait_right_button_press();
	wait_right_button_release();

	printstrln("Press either button 1/2");
	wait_either_button_press();
	wait_all_button_release();

	printstrln("Press either button 2/2");
	wait_either_button_press();
	wait_all_button_release();
	printstrln("==END TESTING BUTTONS==");

}
