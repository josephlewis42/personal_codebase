#include <math.h>
#include <stdio.h>
#include <stdlib.h>

const double EPSILON = 0.0000001;
/**
int main(int argc, char** argv)
{
  const double dt = 1.0, setpoint = 50.0;
  double prev_position = 0.0, error = 0.0, position = 0.0;
  double integral = 0, derivative = 0, output = 0.0; //sum of errors over time
  double Kp = .5, Ki = .3, Kd = .5;
  unsigned int i;

  if(argc != 4){
    fprintf(stderr, "usage: %s <Kp> <Ki> <Kd>\n", argv[0]);
    return 1;
  }

  Kp = atof(argv[1]);
  Ki = atof(argv[2]);
  Kd = atof(argv[3]);

  fprintf(stdout, "# setpoint = %f, initial = %f, Kp = %f, Ki = %f, Kd = %f\n",
	  setpoint, position, Kp, Ki, Kd);

  i = 1;
  fprintf(stdout, "%u\t%f\n", i, position);

  while(fabs(setpoint - position) > EPSILON){
      error = setpoint - position;
      integral = integral + error*dt;
      derivative = (position - prev_position)/dt;

      output = (Kp*error) + (Ki*integral) + (Kd*derivative);

      prev_position = position; // for derivitive
      position += output; //Plant is itegral 1/s
      fprintf(stdout, "%u\t%f\n", i, position);
      i++;
  }
  return 0;
}
**/
