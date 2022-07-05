/* This is for testing depressing synaptic current*/
/* Coupling regualr spiking neuron with simple alpha function model */
/* 
The AdEx model is from 
"Firing patterns in the adaptive exponential integrage-and-fire model" R Naud, N Marcille, C Colpath and W Gerstner, Biol Cybern, 2008

The parameters are the same as figure 4a, those are specified in table 1 in the paper.

written by Joon Ho Choi, 
2019 October 30
*/
#ifndef _ADEX_EQU_

#define _ADEX_EQU_

#define getrandom(maxInt) ((rand()%(int)((maxInt)))) 
#define HIST 400

typedef struct {
  double v, w;
  double C, g_L, E_L, V_T, del_T, a, tau_w, b, V_r, psc_amp, psc_tau;
  double F1stCo, S2ndCo, T3rdCo, F5thCo, S6thCo;
  double input[HIST];		/* list of synaptic input that will be updated*/
  int *post;  		/* list of connected cells, inhibitory number is selected because it is bigger */
  double *weight;        /* list of synaptic weight to post[n], inhibitory number is selected because it is bigger */
} neuron;

int equations(neuron *n);
int PSC_mapping(neuron *n, double w, neuron *post);
double Gauss_noise(double sigma); /* From AdEx_equations_1.1.c */

#else

#endif
