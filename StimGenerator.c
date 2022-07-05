#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char **argv)
{
  int i = 0;
  float amp = 1, period = 1000.0, duration = 10000;

  if(argc == 3){
    sscanf(*(argv +1), "%f", &amp);
    sscanf(*(argv +2), "%f", &duration);
  } else {
    fprintf(stderr, "USAGE : %s <amplitude> <duration(ms)>!!!\n", *(argv +0));
    exit(1);
  }
  
  printf("0\n");
  for (i=0; i < duration; i++)
    {
      printf("%.3f\n", amp * sin(3.1416 * i / period)*sin(3.1416 * i / period));;
    }

  return 0;
}
