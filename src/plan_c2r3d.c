#include <mpi.h>
#include <fftw3-mpi.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(int argv, char **argc)
{
    int rank, size;
    fftw_complex *in;
    double *out;
    double *data;
    double *res;
    fftw_plan plan;
    int sumrecv = 0;
    ptrdiff_t alloc_local, local_n0, local_0_start, i, j, k;
    int *data_size_on_cores;
    int L =10; 
    int M =10; 
    int N =10;
    int mpi_tag = 123;
    double *buf;
    int irank;
    MPI_Status status;
    double t0, t1, t2;

    MPI_Init(&argv, &argc);
    fftw_mpi_init();

    MPI_Comm_rank (MPI_COMM_WORLD, &rank);
	MPI_Comm_size (MPI_COMM_WORLD, &size);

    t0 = MPI_Wtime ();
    alloc_local = fftw_mpi_local_size_3d(L, M, N/2+1, MPI_COMM_WORLD, &local_n0, &local_0_start);
	printf("size  %td  %d\n", alloc_local, L*M*(N/2+1));

	out  = fftw_alloc_real(2*alloc_local);
	in = fftw_alloc_complex(alloc_local);
	if (rank ==0) res  = malloc(L*M*N*sizeof(double));
	data_size_on_cores = malloc(size*sizeof(int));
	buf   = malloc(((L/size)+1)*M*N*sizeof(double));
	data  = malloc(L*M*(N/2+1)*2*sizeof(double));

	for (i =0; i<L; ++i)
		for (j =0; j<M; ++j)
			for (k =0; k<N/2+1; ++k){
				data[(i*L+j)*M+2*k]   = (double)(i+j+k);
				data[(i*L+j)*M+2*k+1] = (double)(i+j+k+5.);}
		
	for (i =0; i<size; ++i) data_size_on_cores[i] = round(L/size);	
	if (round(L/size)!= L/size){
		int nc = 0; 
		for (i = L/size - round(L/size); i>0; --i ){ 
			 data_size_on_cores[nc] +=1;
			 nc +=1;
		   }
	 }
   for (i =0; i<size; ++i) data_size_on_cores[i] = data_size_on_cores[i]*M*N;
   MPI_Barrier (MPI_COMM_WORLD);
   t1 = MPI_Wtime();
   plan = fftw_mpi_plan_dft_c2r_3d(L, M, N/2+1, in, out, MPI_COMM_WORLD, FFTW_MEASURE);  
   MPI_Barrier (MPI_COMM_WORLD);
   
   for (i = 0; i < local_n0; ++i) 
       for (j = 0; j < M; ++j) 
    	   for (k= 0; k< N/2+1; ++k){
			   in[(i*M+j)*(N/2+1)+k][0] = data[((i+local_0_start)*M+j)*N +2*k];
			   in[(i*M+j)*(N/2+1)+k][1] = data[((i+local_0_start)*M+j)*N +2*k+1];}
			   
	fftw_free (data);
	MPI_Barrier (MPI_COMM_WORLD);
	if (rank == 0) printf("Before FFT is %gs with %d procs\n", t1-t0, size);
    fftw_execute(plan);
    MPI_Barrier (MPI_COMM_WORLD);
    fftw_free (in);
    t2 = MPI_Wtime ();
    if (rank == 0) printf("Loop time is %gs with %d procs\n", t2-t1, size);
    if (rank == 0) {
    	   for (i = 0; i <data_size_on_cores[rank]; ++i) { 
    	       res[sumrecv]   = out[i];
    	       sumrecv   +=1;}
      }
     if (size >1){ 
     for (irank =1; irank<size; ++irank)
        if (rank ==irank) MPI_Send(out, data_size_on_cores[irank],  MPI_DOUBLE, 0, mpi_tag, MPI_COMM_WORLD);
    	else continue;
     if (rank == 0){ 
         for (irank =1; irank<size; ++irank){
            MPI_Recv(buf, data_size_on_cores[irank], MPI_DOUBLE, irank, mpi_tag, MPI_COMM_WORLD, &status);
            for (i = 0; i <data_size_on_cores[irank]; ++i){ 
              res[sumrecv]   = buf[i];
    	      sumrecv +=1;}
    	 }
      }
   }
    if (rank == 0){
      int nc  = 0; 
      for (i = 0; i < L; ++i) 
        for (j = 0; j < M; ++j) 
    	  for (k= 0; k< N; ++k){
    	  	  printf("value %d %lf\n", nc, res[(i*M+j)*N+k]);
    	  	  nc +=1;}
    	}
    MPI_Barrier (MPI_COMM_WORLD);
    fftw_free(out);
    fftw_free(buf);
    fftw_destroy_plan(plan);
    MPI_Finalize();
    return 0;
}
