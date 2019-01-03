#include <fftw3.h>
#include <stdio.h>
#include <math.h>
#define REAL 0
#define IMAG 1
int main(int argc, char **argv)
{
   
   fftw_complex *in, *out;
   fftw_plan p;
   ptrdiff_t N, i, j;
  
    N = 800;
   in  = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
   out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
   p   = fftw_plan_dft_1d(N, in, out, FFTW_FORWARD, FFTW_ESTIMATE);
   for (i = 0; i < N; ++i)
       in[i][0] = cos(i*M_PI/N);
       in[i][1] = 0.0;
   fftw_execute(p);
   fftw_destroy_plan(p);
   fftw_free(in);
   fftw_free(out);
   }