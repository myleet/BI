#include <mpi.h>
#include <fftw3-mpi.h>
#include <stdio.h>
#include <math.h>
#define REAL 0
#define IMAG 1
int main(int argc, char **argv) {
    //const ptrdiff_t N0 = 48000, N1 = 48000;
    int rank, size;
    ptrdiff_t N0  = 15;
    ptrdiff_t N1  = 10;
    fftw_plan plan;
    fftw_complex *cout;
    double *rin;
    ptrdiff_t alloc_local, local_n0, local_0_start, i, j;
    double *res;
    int *data_size_on_cores;
    int mpi_tag = 123;
    double *buf;
    int irank;
    double *data;
    int sumrecv = 0;
    MPI_Status status;
    MPI_Init(&argc, &argv);
    fftw_mpi_init();
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);
	MPI_Comm_size (MPI_COMM_WORLD, &size);
    /* get local data size and allocate */
    
    alloc_local = fftw_mpi_local_size_2d(N0, N1/2+1, MPI_COMM_WORLD, &local_n0, &local_0_start);
    rin  = fftw_alloc_real(2* alloc_local);
    cout = fftw_alloc_complex(alloc_local);
    buf  = malloc(((N0/size)+1)*2*(N1/2+1)*sizeof(double));
    if (rank ==0) res = malloc(N0 * ((N1/2+1)*2)*sizeof(double));
    data  = malloc(N0*N1*sizeof(double));
	data_size_on_cores = malloc(size*sizeof(int));
	
	for (i=0; i<N0; ++i)
		for (j=0; j<N1; ++j)
			data[i*N1+j] = (double)(i+j);
			
	for (i =0; i<size; ++i) data_size_on_cores[i] = round(N0/size);
		
	if (round(N0/size)!= N0/size) {
		int nc = 0; 
		for (i = N0/size - round(N0/size); i>0; --i ) { 
			 data_size_on_cores[nc] +=1;
			 nc +=1;
		   }
	 }
	for (i =0; i<size; ++i) data_size_on_cores[i] = data_size_on_cores[i]*(N1/2+1)*2;
          	 
    /* create plan for in-place forward DFT */
    plan = fftw_mpi_plan_dft_r2c_2d(N0, N1, rin, cout, MPI_COMM_WORLD, FFTW_MEASURE);
    
      for (i = 0; i < local_n0; ++i)
        for (j = 0; j < N1; ++j)
          rin[i*(N1/2+1)*2 + j] = data[(i+local_0_start)*N1+j];  
    
    MPI_Barrier (MPI_COMM_WORLD);
    // compute transforms, in-place, as many times as desired */
    fftw_execute(plan);
    MPI_Barrier (MPI_COMM_WORLD);
   if (rank == 0) {
    	   for (i = 0; i <data_size_on_cores[rank]/2; ++i) { 
    	       res[sumrecv]   = cout[i][0];
    	       res[sumrecv+1] = cout[i][1];
    	       sumrecv   +=2;  
    	   }
     }
 if (size >1) { 
     for (irank =1; irank<size; ++irank)
        if (rank ==irank) MPI_Send(cout, data_size_on_cores[irank],  MPI_DOUBLE, 0, mpi_tag, MPI_COMM_WORLD);
    	else continue;
     if (rank == 0) { 
         for (irank =1; irank<size; ++irank) {
            MPI_Recv(buf, data_size_on_cores[irank], MPI_DOUBLE, irank, mpi_tag, MPI_COMM_WORLD, &status);
            for (i = 0; i <data_size_on_cores[irank]/2; ++i) { 
              res[sumrecv]   = buf[2*i];
    	      res[sumrecv+1] = buf[2*i+1];
    	      sumrecv +=2; 
    	     }
    	 }
      }
   } 
   MPI_Barrier (MPI_COMM_WORLD);
   if (rank == 0) {  
       for (i = 0; i <N0; ++i) 
       		for (j =0; j < N1/2+1; ++j)	
    	       printf("Qvalue is %lf  %lf\n", res[i*(N1/2+1)*2+ 2*j], res[i*(N1/2+1)*2+ 2*j+1]); }
    MPI_Barrier (MPI_COMM_WORLD);
    fftw_destroy_plan(plan);
    MPI_Finalize();
}