#!/usr/bin/env python
#
#
#  08/26/2016
#  New version of sort3D.
#  
from    math  	         import  *
from    myfftwmpi        import  *
import numpy as np
mpi_init(0, [])
print("Program starts!")
myid  = mpi_comm_rank(MPI_COMM_WORLD)
nproc = mpi_comm_size(MPI_COMM_WORLD)
print("myid", myid, nproc)
mpi_barrier(MPI_COMM_WORLD)
L =10
M= 10
N =10
res  = ""
import types
mpi_barrier(MPI_COMM_WORLD)
if myid ==0: a =1
else: a =0
a = mpi_bcast(a, 1, MPI_INT, 0, MPI_COMM_WORLD)
print(a)
res = do_mpi_fftwc2r_3d(L, M, N, myid, nproc, MPI_COMM_WORLD)
print(res)
mpi_barrier(MPI_COMM_WORLD)
"""
if myid ==0:
	res.tolist()
	for i in range(len(res)):
		if res[i] !=0.0:
			print (" index %d   value %f"%(i, res[i]))
"""
mpi_finalize()
exit()