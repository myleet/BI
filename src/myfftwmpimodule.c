#include <Python.h>
#include <mpi.h>
#include <fftw3-mpi.h>
#define NUMPY
#define DATA_TYPE long
#define COM_TYPE  long
#define ARG_ARRAY
//#define PyMODINIT_FUNC void
//#ifndef PyMODINIT_FUNC
//#define PyMODINIT_FUNC void
#define CAST long
#define VERT_FUNC PyInt_FromLong
#define ARG_ARRAY
#define DATA_TYPE long
#define COM_TYPE  long
#undef DO_UNSIGED

#ifdef  NUMPY
	#include <numpy/arrayobject.h>
	#define LIBRARY "NUMPY"
#else
	#include <Numeric/arrayobject.h>
	#define LIBRARY "Numeric"
#endif

#ifdef LAM
	#define NULL_INIT
#endif

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <sys/types.h>
#define PyMODINIT_FUNC
/*
  C wrapper of FFTW3/FFTW3 MPI and openmpi functions for python
  Copyright (c) 2018 Zhong Huang ; Email: zhuangdvm@gmail.com
  All Rights Reserved
*/



int get_type(long mpitype);
int ierr;
int erroron;
static PyObject *myfftwmpiError;

static PyObject *mpi_init(PyObject *self, PyObject *args)
{
  PyObject *input;
  int did_it;
  int argc = 0, i, n;
  char **argv;
  
  #ifdef ARG_STR
	char *argstr;
	int *strides;
	int arglen;
 #endif
 
 #ifdef SIZE_RANK
	PyArrayObject *result;
	int dimensions[1],data[2];
	char *aptr;
	int numprocs, myid;
 #endif
 
 #ifdef ARG_ARRAY
	PyObject *result;
 #endif
  
	int len;
	argv    = NULL;
	erroron = 0;
	char error_message[1024];
   
      ierr = MPI_Initialized(&did_it);
	  if(!did_it){
			if (!PyArg_ParseTuple(args, "iO", &argc, &input)) return NULL;
			argv=(char**)malloc((argc+2)*sizeof(char*));
			if (argv == NULL) {
				sprintf(error_message, "BAD_ALLOC: In mpi_init(), malloc() failed to allocate %lu bytes to pointer argv.\n", (argc+2)*sizeof(char*));
				perror(error_message);
			}
			n=PyList_Size(input);
			for(i=0;i<n;i++) {
				len=strlen(PyString_AsString(PyList_GetItem(input,i)));
				argv[i]=(char*)malloc(len+1);
				if (argv[i] == NULL) {
					sprintf(error_message, "BAD_ALLOC: In mpi_init(), malloc() failed to allocate %d bytes to pointer argv[i].\n", len+1);
					perror(error_message);
				}
				argv[i][len]=(char)0;
				strncpy(argv[i],PyString_AsString(PyList_GetItem(input,i)),(size_t)len);
				/* printf("%s ",argv[i]); */
			}
			#ifdef NULL_INIT
			   ierr = MPI_Init(NULL, NULL);
			#else
			   ierr = MPI_Init(&argc, &args);
			   printf("NO NULL\n");
			#endif
		#ifdef MPI2
			MPI_Comm_create_errhandler( eh, &newerr );
		#endif	
	   }
	#ifdef ARG_STR
			arglen=0;
			strides=(int*)malloc(argc*sizeof(int));
			if (strides == NULL) {
				sprintf(error_message, "BAD_ALLOC: In mpi_init(), malloc() failed to allocate %d bytes to pointer strides.\n", argc*sizeof(int));
				perror(error_message);
			}
			strides[0]=0;
			for(i=0;i<argc;i++) {
				arglen=arglen+strlen(argv[i])+1;
				strides[i+1]=strides[i]+strlen(argv[i])+1;
			}
			argstr=(char*)malloc(arglen*sizeof(char));
			if (argstr == NULL) {
				sprintf(error_message, "BAD_ALLOC: In mpi_init(), malloc() failed to allocate %d bytes to pointer argstr.\n", arglen*sizeof(char));
				perror(error_message);
			}
			for(i=0;i<argc;i++) {
				for(n=0;n<strlen(argv[i]);n++) {
					argstr[strides[i]+n]=argv[i][n];
				}
				argstr[strides[i]+strlen(argv[i])]=(char)32;
	/*
				free(argv[i]);
	*/
			}
			return PyString_FromString(argstr);
	#endif

	#ifdef ARG_ARRAY
			result = PyTuple_New(argc);
			for(i=0;i<argc;i++) {
				PyTuple_SetItem(result,i,PyString_FromString(argv[i]));
			}
			return result;
	#endif

	#ifdef SIZE_RANK
		ierr=MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
		ierr=MPI_Comm_rank(MPI_COMM_WORLD,&myid);
		dimensions[0]=2;
		result = (PyArrayObject *)PyArray_FromDims(1, dimensions, PyArray_INT);
		if (result == NULL)
			return NULL;
		data[0] = myid;
		data[1] = numprocs;
		aptr=(char*)&(data);
		for(i=0;i<8;i++)
			result->data[i]=aptr[i];
		if(erroron){ erroron=0; return NULL;}
		return PyArray_Return(result);
	#endif
}

static PyObject *mpi_comm_rank(PyObject *self, PyObject *args)
{
  long comm;
  int rank;
  if (!PyArg_ParseTuple(args, "l",&comm)) return NULL;
  ierr = MPI_Comm_rank((MPI_Comm)comm,&rank);
  return PyInt_FromLong((long)rank);
}
static PyObject *mpi_comm_size(PyObject *self, PyObject *args)
{
/* int MPI_Probe( int source, int tag, MPI_Comm comm, MPI_Status *status ) */
long comm;
int numprocs;

	if (!PyArg_ParseTuple(args, "l", &comm)) return NULL;
	ierr = MPI_Comm_size((MPI_Comm)comm,&numprocs);
	return PyInt_FromLong((long)numprocs);
}

static PyObject * mpi_finalize(PyObject *self, PyObject *args) {
	if(erroron){ erroron=0; return NULL;}
    return PyInt_FromLong((long)MPI_Finalize());
}

static PyObject *mpi_barrier(PyObject *self, PyObject *args)
{
long comm;
 if (!PyArg_ParseTuple(args, "l", &comm)) return NULL;
  ierr = MPI_Barrier((MPI_Comm)comm );
  return PyInt_FromLong((long)ierr);
};


static PyObject *do_mpi_fftwc2r_3d(PyObject *self, PyObject *args)
{
	#define VERT_FUNC PyInt_FromLong
	long finished;
	double *out, *indata, *buf, *res;
	char *aptr;
	int *data_size_on_cores;
	fftw_complex *in;
	fftw_plan plan;
	int sumrecv;
	long alloc_local, local_n0, local_0_start; 
	int i, j, k;
	int mpi_tag, irank, nc;  
	MPI_Status status;
	double t0, t1, t2;
	int nt0, nn, nt;
	int L, M, N;
	int rank, size;
	long comm;
	if (!PyArg_ParseTuple(args, "iiiiil", &L, &M, &N, &rank, &size, &comm)) return NULL;
    printf("my id %d  L %d M %d  N %d \n", rank, L, M, N);
    fftw_mpi_init();
 	npy_intp npsize = L*M*(N/2+1)*2;
 	alloc_local = fftw_mpi_local_size_3d(L, M, N/2+1, (MPI_Comm)comm, &local_n0, &local_0_start);
    t0 = MPI_Wtime ();
    finished = 1L;
    out         = fftw_alloc_real(2*alloc_local);     //fftw_alloc_real(2*alloc_local);
	in          = fftw_alloc_complex(alloc_local);    //fftw_alloc_complex(alloc_local);
	buf         = malloc(2*alloc_local*sizeof(double));//fftw_alloc_real(2*alloc_local);
	mpi_tag  = 123;
	sumrecv  = 0;
	finished = 1;
	printf("alloc_local %td local_0_start %td \n",alloc_local, local_0_start);
 // allocation
	data_size_on_cores = malloc(size*sizeof(int));
	indata  = malloc(L*M*(N/2+1)*2*sizeof(double));
	res     = malloc(L*M*(N/2+1)*2*sizeof(double));
	for (i =0; i <2*alloc_local; ++i) buf[i] = 0.0L;
	for (i =0; i<L*M*(N/2+1)*2;  ++i) res[i] = 0.0L;
	for (i =0; i<2*alloc_local;  ++i) out[i] = 0.0L;
	
	for (i =0; i<L; ++i)
		for (j =0; j<M; ++j)
			for (k =0; k<N/2+1; ++k){
				indata[(i*L+j)*M+2*k]   = (double)(i+j+k);
				indata[(i*L+j)*M+2*k+1] = (double)(i+j+k+5.);}
				
	for (i =0; i<size; ++i) data_size_on_cores[i] = round(L/size);
	if (round(L/size)!= L/size){
		int nc = 0; 
		for (i = L/size - round(L/size); i>0; --i ){ 
			 data_size_on_cores[nc] +=1;
			 nc +=1;
		   }
	 }
   for (i =0; i<size; ++i) data_size_on_cores[i] = data_size_on_cores[i]*M*(N/2+1)*2;
   printf("local size  %td  full size  %d   local_n0 %td    local_0_start %td  myrec %d   \n", alloc_local, L*M*(N/2+1), local_n0, local_0_start, data_size_on_cores[rank]);
   MPI_Barrier ((MPI_Comm)comm);
   t1 = MPI_Wtime();
   nc = 0;
   for (i = 0; i < local_n0; ++i) 
       for (j = 0; j < M; ++j) 
    	   for (k= 0; k< N/2+1; ++k){
			   in[nc][0]   = indata[((i+local_0_start)*M+j)*N +2*k];
			   in[nc][1]   = indata[((i+local_0_start)*M+j)*N +2*k+1];
			   nc +=1;
			    }
	if (rank ==1){
	  for (i = 0; i <alloc_local; ++i)
	     printf("IN  rank %d value %d  %lf %lf \n", rank, i, in[i][0], in[i][1]);}
	     
   plan = fftw_mpi_plan_dft_c2r_3d(L, M, N/2+1, in, out, (MPI_Comm)comm, FFTW_MEASURE);
   
   MPI_Barrier ((MPI_Comm)comm);
	if (rank == 0) printf("Before FFT is %gs with %d procs\n", t1-t0, size);
    fftw_execute(plan);
    MPI_Barrier (comm);
    t2 = MPI_Wtime ();
    //if (rank == 0) printf("Loop time is %gs with %d procs\n", t2-t1, size);
		 if (rank ==0)
		  {
			sumrecv = 0;
			for (i = 0; i <500; ++i) {
			//res[sumrecv] = out[i];
			//buf[i] = out[i];
			sumrecv +=1;
			printf("rank %d value %d  %lf \n", rank, sumrecv, out[i]);
			 }
    	  }
    for (i=0; i <2*alloc_local;  ++i) 
    	printf("rank %d out is %d    %lf   \n",rank, i, out[i]);
    MPI_Barrier (comm);
    /*
     if (size >1){
     if (rank>0) MPI_Send(buf, data_size_on_cores[rank],  MPI_DOUBLE, 0, mpi_tag, (MPI_Comm)comm);
     for (irank =1; irank<size; ++irank){
     	
        if (rank == 0){
            MPI_Recv(buf, data_size_on_cores[rank], MPI_DOUBLE, irank, mpi_tag, (MPI_Comm)comm, &status);
            for (i = 0; i <data_size_on_cores[rank]; ++i){
                 res[sumrecv] = (float) buf[i];
    	         sumrecv +=1;} 
    	        }
    	 }
    }
   MPI_Barrier ((MPI_Comm)comm);
 	aptr = (char *)res;
 	res_arr = (PyArrayObject *) PyArray_SimpleNew(1, &npsize, NPY_FLOAT);
 	for(i=0; i < npsize*sizeof(float);i++) res_arr->data[i] = aptr[i];
 	PyArray_ENABLEFLAGS((PyArrayObject*)res_arr, NPY_ARRAY_OWNDATA);
 	//nn = PyArray_Size(res_arr);
 	//nt = PyArray_NBYTES(res_arr); 
 	//printf("res_arr size is %d\n", nn);
 	//printf("res_arr nt is %d\n", nt);
 	//printf("res_arr nt0 is %d\n", nt0);
 	//printf("cint is %d\n", sizeof(NPY_FLOAT));
 	//printf("cint is %d\n", sizeof(float));}
 	*/
    MPI_Barrier ((MPI_Comm)comm);
    free (in);
    free(indata);
    free(out);
    free(res);
    free(buf);
    fftw_destroy_plan(plan);
    //return PyArray_Return(res_arr);*/
    return PyInt_FromLong(finished);
}

static PyObject * mpi_bcast(PyObject *self, PyObject *args) {
/* int MPI_Bcast ( void *buffer, int count, MPI_Datatype datatype, int root, MPI_Comm comm ) */
int count,root;
DATA_TYPE datatype;
COM_TYPE comm;
int myid;
int mysize;
PyArrayObject *result;
PyArrayObject *array;
PyObject *input;
int dimensions[1];
char *aptr;

	if (!PyArg_ParseTuple(args, "Oilil", &input, &count,&datatype,&root,&comm))
        return NULL;
    dimensions[0] = count;
    result = (PyArrayObject *) PyArray_FromDims(1, dimensions, get_type(datatype));
	aptr=(char*)(result->data);
    ierr = MPI_Comm_rank((MPI_Comm)comm,&myid);
#ifdef MPI2
    if(myid == root || root == MPI_ROOT) {
#else
    if(myid == root) {
#endif
		array = (PyArrayObject *) PyArray_ContiguousFromObject(input, get_type(datatype), 0, 3);
		if (array == NULL)
			return NULL;
		ierr=MPI_Type_size((MPI_Datatype)datatype,&mysize);
		memcpy((void *)(result->data), (void*)array->data, (size_t) (mysize*count));
		Py_DECREF(array);
	}
	ierr=MPI_Bcast(aptr,count,(MPI_Datatype)datatype,root,(MPI_Comm)comm);
#ifdef DEBUG
	if(count >0)
		writeit(result,count,(MPI_Datatype)datatype,"bcast");
	else
		dummy("bcast");
#endif
  	return PyArray_Return(result);
}
/*//Some new functions
static PyObject *new_vec(PyObject *self, PyObject *args) {
  // expect a single integer argument
  int i, n;
  if (!(PyArg_ParseTuple(args, "i", &n))) return NULL;
  // create the array in C on the heap
  int *array = NULL;
  if (!(array = malloc(n * sizeof(int)))) return NULL;
  for (i = 0; i < n; ++i) array[i] = i;
  // return the array as a numpy array (numpy will free it later)
  npy_intp dims[1] = {n};
  PyObject *narray = PyArray_SimpleNewFromData(1, dims, NPY_INT, array);
  // this is the critical line - tell numpy it has to free the data
  PyArray_ENABLEFLAGS((PyArrayObject*)narray, NPY_ARRAY_OWNDATA);
  return narray;
}*/

int get_type(long mpitype) {
	if(mpitype == (long)MPI_INT)    return(PyArray_INT);
	if(mpitype == (long)MPI_FLOAT)  return(PyArray_FLOAT);
	if(mpitype == (long)MPI_DOUBLE) return(PyArray_DOUBLE);
	if(mpitype == (long)MPI_CHAR)   return(PyArray_CHAR);  /* Added in version for sparx */
	printf("could not find type input: %ld  available: MPI_FLOAT %ld MPI_INT %ld MPI_DOUBLE %ld MPI_CHAR %ld\n",mpitype,(long)MPI_FLOAT,(long)MPI_INT,(long)MPI_DOUBLE,(long)MPI_CHAR);
	return(PyArray_INT);
}

static PyMethodDef myfftwmpiMethods[] = {
    {"do_mpi_fftwc2r_3d",  do_mpi_fftwc2r_3d, METH_VARARGS, "do_mpi_fftwc2r_3d"},
    {"mpi_init",        mpi_init,       METH_VARARGS, "mpi_init"},
    {"mpi_comm_rank",   mpi_comm_rank,  METH_VARARGS, "mpi_comm_rank"},
    {"mpi_finalize",    mpi_finalize,   METH_VARARGS, "mpi_finalize"},
    {"mpi_barrier",     mpi_barrier,    METH_VARARGS, "mpi_barrier"},
    {"mpi_comm_size",   mpi_comm_size,  METH_VARARGS, "mpi_comm_size"},
    {"mpi_bcast",       mpi_bcast,      METH_VARARGS,  "mpi_bcast"},
   // {"new_vec",         new_vec,        METH_VARARGS,  "new_vec"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC void initmyfftwmpi(){
  import_array();
  PyObject *m;
  PyObject *tmp, *d;
  m = Py_InitModule("myfftwmpi", myfftwmpiMethods);
  d = PyModule_GetDict(m);
  myfftwmpiError = PyErr_NewException("myfftwmpi.error", NULL, NULL);
  PyModule_AddObject(m, "error", myfftwmpiError);
  Py_INCREF(myfftwmpiError);
  tmp = VERT_FUNC((CAST)MPI_COMM_WORLD);
  PyDict_SetItemString(d,   "MPI_COMM_WORLD", tmp);  Py_DECREF(tmp);
  
    tmp = VERT_FUNC((CAST)MPI_CHAR);
    PyDict_SetItemString(d,   "MPI_CHAR", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_BYTE);
    PyDict_SetItemString(d,   "MPI_BYTE", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_SHORT);
    PyDict_SetItemString(d,   "MPI_SHORT", tmp);  Py_DECREF(tmp);
    
    
  tmp = VERT_FUNC((CAST)MPI_INT);
  PyDict_SetItemString(d,   "MPI_INT", tmp);  Py_DECREF(tmp);
  tmp = VERT_FUNC((CAST)MPI_LONG);
  PyDict_SetItemString(d,   "MPI_LONG", tmp);  Py_DECREF(tmp);
  tmp = VERT_FUNC((CAST)MPI_FLOAT);
  PyDict_SetItemString(d,   "MPI_FLOAT", tmp);  Py_DECREF(tmp);
  tmp = VERT_FUNC((CAST)MPI_DOUBLE);
  PyDict_SetItemString(d,   "MPI_DOUBLE", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_FLOAT_INT);
    PyDict_SetItemString(d,   "MPI_FLOAT_INT", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_LONG_INT);
    PyDict_SetItemString(d,   "MPI_LONG_INT", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_DOUBLE_INT);
    PyDict_SetItemString(d,   "MPI_DOUBLE_INT", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_SHORT_INT);
    PyDict_SetItemString(d,   "MPI_SHORT_INT", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_2INT);
    PyDict_SetItemString(d,   "MPI_2INT", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_LONG_DOUBLE_INT);
    PyDict_SetItemString(d,   "MPI_LONG_DOUBLE_INT", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_LONG_LONG_INT);
    PyDict_SetItemString(d,   "MPI_LONG_LONG_INT", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_PACKED);
    PyDict_SetItemString(d,   "MPI_PACKED", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_Pack);
    PyDict_SetItemString(d,   "MPI_Pack", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_Unpack);
    PyDict_SetItemString(d,   "MPI_Unpack", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_UB);
    PyDict_SetItemString(d,   "MPI_UB", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_LB);
    PyDict_SetItemString(d,   "MPI_LB", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_MAX);
    PyDict_SetItemString(d,   "MPI_MAX", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_MIN);
    PyDict_SetItemString(d,   "MPI_MIN", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_SUM);
    PyDict_SetItemString(d,   "MPI_SUM", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_PROD);
    PyDict_SetItemString(d,   "MPI_PROD", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_LAND);
    PyDict_SetItemString(d,   "MPI_LAND", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_BAND);
    PyDict_SetItemString(d,   "MPI_BAND", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_LOR);
    PyDict_SetItemString(d,   "MPI_LOR", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_BOR);
    PyDict_SetItemString(d,   "MPI_BOR", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_LXOR);
    PyDict_SetItemString(d,   "MPI_LXOR", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_BXOR);
    PyDict_SetItemString(d,   "MPI_BXOR", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_MAXLOC);
    PyDict_SetItemString(d,   "MPI_MAXLOC", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_COMM_NULL);
    PyDict_SetItemString(d,   "MPI_COMM_NULL", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_OP_NULL);
    PyDict_SetItemString(d,   "MPI_OP_NULL", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_GROUP_NULL);
    PyDict_SetItemString(d,   "MPI_GROUP_NULL", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_DATATYPE_NULL);
    PyDict_SetItemString(d,   "MPI_DATATYPE_NULL", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_REQUEST_NULL);
    PyDict_SetItemString(d,   "MPI_REQUEST_NULL", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_ERRHANDLER_NULL);
    PyDict_SetItemString(d,   "MPI_ERRHANDLER_NULL", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_MAX_PROCESSOR_NAME);
    PyDict_SetItemString(d,   "MPI_MAX_PROCESSOR_NAME", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_MAX_ERROR_STRING);
    PyDict_SetItemString(d,   "MPI_MAX_ERROR_STRING", tmp);  Py_DECREF(tmp);
	tmp = PyInt_FromLong((long)MPI_UNDEFINED);
    PyDict_SetItemString(d,   "MPI_UNDEFINED", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_KEYVAL_INVALID);
    PyDict_SetItemString(d,   "MPI_KEYVAL_INVALID", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_BSEND_OVERHEAD);
    PyDict_SetItemString(d,   "MPI_BSEND_OVERHEAD", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_PROC_NULL);
    PyDict_SetItemString(d,   "MPI_PROC_NULL", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_ANY_SOURCE);
    PyDict_SetItemString(d,   "MPI_ANY_SOURCE", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_ANY_TAG);
    PyDict_SetItemString(d,   "MPI_ANY_TAG", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_BOTTOM);
    PyDict_SetItemString(d,   "MPI_BOTTOM", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_COMM_WORLD);
    PyDict_SetItemString(d,   "MPI_COMM_WORLD", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_TAG_UB);
    PyDict_SetItemString(d,   "MPI_TAG_UB", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_HOST);
    PyDict_SetItemString(d,   "MPI_HOST", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_IO);
    PyDict_SetItemString(d,   "MPI_IO", tmp);  Py_DECREF(tmp);
    tmp = VERT_FUNC((CAST)MPI_WTIME_IS_GLOBAL);
    PyDict_SetItemString(d,   "MPI_WTIME_IS_GLOBAL", tmp);  Py_DECREF(tmp);
    tmp = PyString_FromString(LIBRARY);
    PyDict_SetItemString(d,   "ARRAY_LIBRARY", tmp);  Py_DECREF(tmp);
  };