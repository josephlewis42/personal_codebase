#ifndef SERVOS_H_FILE
#define SERVOS_H_FILE

void servo_task(unsigned int timeout_ticks); // launches the servo task, timeout turns it off timeout=0 for continueous.
void left_forward(int pct);
void left_reverse(int pct);

void right_forward(int pct);
void right_reverse(int pct);

void right_stop();
void left_stop();


#endif
