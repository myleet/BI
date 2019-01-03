#include <mpi.h>
#include <fftw3-mpi.h>
#include <stdio.h>
#include <math.h>
#define REAL 0
#define IMAG 1
#define N0  100
#define N1  100
int main(int argc, char **argv)
{
	int rank, size;
    fftw_plan plan;
    fftw_complex *data;
    ptrdiff_t alloc_local, local_n0, local_0_start, i, j;
    MPI_Init(&argc, &argv);
    fftw_mpi_init();
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);
	MPI_Comm_size (MPI_COMM_WORLD, &size);
    alloc_local = fftw_mpi_local_size_2d(N0, N1, MPI_COMM_WORLD, &local_n0, &local_0_start);
	data = fftw_alloc_complex(alloc_local);    
    plan = fftw_mpi_plan_dft_2d(N0, N1, data, data, MPI_COMM_WORLD, FFTW_FORWARD, FFTW_ESTIMATE);
    for (i = 0; i < local_n0; ++i) 
    	for (j = 0; j < N1; ++j)
			data[i*N1+j][0] = (double)(i+j);
			data[i*N1+j][1] = (double)(i);
	MPI_Barrier (MPI_COMM_WORLD);
    /* compute transforms, in-place, as many times as desired */
       for (i = 0; i < local_n0; ++i)
    	 for (j = 0; j < N1; ++j)
    	 	 printf("alloc_local1 is %f\n" ,data[i*N1+j][0]);
    	 	 printf("alloc_local1 is %f\n" ,data[i*N1+j][1]);
    fftw_execute(plan);
    for (i = 0; i < local_n0; ++i)
    	 for (j = 0; j < N1; ++j)
    	 	 printf("alloc_local2 is %f\n" ,data[i*N1+j][0]);
    	 	 printf("alloc_local2 is %f\n" ,data[i*N1+j][1]);
    fftw_destroy_plan(plan);
    fftw_free(data);
    MPI_Finalize();
}