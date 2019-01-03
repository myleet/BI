#include <mpi.h>
#include <fftw3-mpi.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(int argv, char **argc)
{
    int rank, size;
    double *in;
    fftw_complex *out;
    double *res;
    fftw_plan plan;
    int sumrecv = 0;
    ptrdiff_t alloc_local, local_n0, local_0_start, i, j , k;
    int *data_size_on_cores;
    int L =760; 
    int M =760; 
    int N =760;
    double *data;
    int mpi_tag = 123;
    double *buf;
    int irank;
    MPI_Status status;
    double t0, t1, t2;

    MPI_Init(&argv, &argc);
    fftw_mpi_init();

    MPI_Comm_rank (MPI_COMM_WORLD, &rank);
	MPI_Comm_size (MPI_COMM_WORLD, &size);
	
    MPI_Barrier (MPI_COMM_WORLD);
    t0 = MPI_Wtime ();
    
    alloc_local = fftw_mpi_local_size_3d(L, M, N/2+1, MPI_COMM_WORLD, &local_n0, &local_0_start);
	in  = fftw_alloc_real(2*alloc_local);
	out = fftw_alloc_complex(alloc_local);
	if (rank ==0) res  = malloc(L*M*((N/2+1)*2)*sizeof(double));
	data_size_on_cores = malloc(size*sizeof(int));
	buf  = malloc(((L/size)+1)*M*2*(N/2+1)*sizeof(double));
	data  = malloc(L*M*N*sizeof(double));
	
	for (i =0; i<L; ++i)
		for (j =0; j<M; ++j)
			for (k =0; k<N; ++k)
				data[(i*L+j)*M+k] = (double)(i+j+k);
					
	for (i =0; i<size; ++i) data_size_on_cores[i] = round(L/size);	
	if (round(L/size)!= L/size) {
		int nc = 0; 
		for (i = L/size - round(L/size); i>0; --i ) { 
			 data_size_on_cores[nc] +=1;
			 nc +=1;
		   }
	 }
   for (i =0; i<size; ++i) data_size_on_cores[i] = data_size_on_cores[i]*(N/2+1)*2*M;
   MPI_Barrier (MPI_COMM_WORLD);
   t1 = MPI_Wtime ();
   plan = fftw_mpi_plan_dft_r2c_3d(L, M, N, in, out, MPI_COMM_WORLD, FFTW_MEASURE);  
   MPI_Barrier (MPI_COMM_WORLD);
   for (i = 0; i < local_n0; ++i) 
       for (j = 0; j < M; ++j) 
    	   for (k= 0; k< N; ++k)
			   in[(i*M+j)*(N/2+1)*2+k] = data[((i+local_0_start)*M+j)*N +k];
	fftw_free (data);
	
	MPI_Barrier (MPI_COMM_WORLD);
	if (rank == 0) printf("Before FFT is %gs with %d procs\n", t1-t0, size);
    fftw_execute(plan);
    MPI_Barrier (MPI_COMM_WORLD);
    fftw_free (in);
    t2 = MPI_Wtime ();
    if (rank == 0) printf("Loop time is %gs with %d procs\n", t2-t1, size);
    if (rank == 0) {
    	   for (i = 0; i <data_size_on_cores[rank]/2; ++i) { 
    	       res[sumrecv]   = out[i][0];
    	       res[sumrecv+1] = out[i][1];
    	       sumrecv   +=2;  
    	   }
     }
     if (size >1) { 
     for (irank =1; irank<size; ++irank)
        if (rank ==irank) MPI_Send(out, data_size_on_cores[irank],  MPI_DOUBLE, 0, mpi_tag, MPI_COMM_WORLD);
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
    fftw_free (out);
    fftw_free (buf);
    fftw_destroy_plan (plan);
    MPI_Finalize();
    return 0;
}
