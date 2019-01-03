#include <fftw3.h>
#include <stdio.h>
#include <math.h>
#define REAL 0
#define IMAG 1
int main(int argc, char **argv)
{
    //const ptrdiff_t N0 = 48000, N1 = 48000;
    ptrdiff_t N1 =  100;
    fftw_plan plan;
    fftw_complex *cout;
    double *rin;
    ptrdiff_t alloc_local, local_n0, local_0_start, i, j;
    /* get local data size and allocate */
    alloc_local = fftw_mpi_local_size_1d(N, MPI_COMM_WORLD, &local_n0, &local_0_start);
    
    rin  = fftw_alloc_real(2* alloc_local);
    cout = fftw_alloc_complex(alloc_local);
    
    if (rank == 0) 
    	{ 
    	  printf("current rin size is %td\n", 2*alloc_local);
    	  printf("current cout size is %td\n", alloc_local);
    	  printf("current cout size is %td\n", local_n0);
    	 }
    /* create plan for in-place forward DFT */
    plan = fftw_plan_dft_r2c_1d(N1, rin, cout, MPI_COMM_WORLD, FFTW_MEASURE);
    
    for (i = 0; i < local_n0; ++i) for (j = 0; j < 2*(N1/2+1); ++j)
       rin[i*(N1/2+1)*2 + j] = 0.0;
                                
    for (i = 0; i < local_n0; ++i) for (j = 0; j < N1; ++j)
       rin[i*(N1/2+1)*2 + j] = (double)(i+j);
    
    MPI_Barrier (MPI_COMM_WORLD);
    /* compute transforms, in-place, as many times as desired */
    fftw_execute(plan);
    MPI_Barrier (MPI_COMM_WORLD);
    
    
    if (rank == 0)
    	{
    		for (i = 0; i < local_n0; ++i) 
    			for (j = 0; j <(N1/2+1); ++j)
    				{
    			  		//printf("index is  %td\n", (i*(N1/2+1)+j));
    			  		printf("value is %lf  %lf\n", cout[i*(N1/2+1)+j][0], cout[i*(N1/2+1)+j][1]);
    				}
    	}
    
        if (rank == 1)
    	{
    	   printf("rank %d/n", rank);
    		for (i = 0; i < local_n0; ++i) 
    			for (j = 0; j <(N1/2+1); ++j)
    				{
    			  		//printf("index is  %td\n", (i*(N1/2+1)+j));
    			  		printf("value is %lf  %lf\n", cout[i*(N1/2+1)+j][0], cout[i*(N1/2+1)+j][1]);
    				}
    	}    
    MPI_Barrier (MPI_COMM_WORLD);
    fftw_destroy_plan(plan);
    MPI_Finalize();
}