import gc
import geometry, fourier, sigproc
import numpy as n
import objectives.cudaworker as cudaworker
import pycuda.gpuarray as gpuarray
###
# find default parameters from default.params
#
import os
import symmetry


def compute_symmetry_errs(rs,symop,gfV,gfVnopre,radwn,stream=None):
    N = gfV[0].shape[0]
    offRs = geometry.expmaps(rs)
    Rsyms = symop.get_rotations(include_identity=False)
    pts   = geometry.gencoords(N, 3, radwn).reshape((-1,3))

    N_R = offRs.shape[0]
    N_S = 1
    N_T = pts.shape[0]
    N_T_aligned = int(n.ceil(float(N_T)/(2*cudaworker.cukrns.blocksize)))*(2*cudaworker.cukrns.blocksize)
    print('   ')
    print('NR, NS, NT ', N_R, N_S, N_T, N_T_aligned, (N_R*N_T_aligned)/1.e9)
    with cudaworker.GPUContext():
        gts = gpuarray.zeros((1,3),n.float32)
        gret = gpuarray.zeros((N_R,N_S),n.float32)
        gphis = gpuarray.empty((N_R,N_S),n.float32)
        gP = (gpuarray.empty((N_R,N_T_aligned),n.float32),
              gpuarray.empty((N_R,N_T_aligned),n.float32))
        gQ = (gpuarray.empty((1,N_T_aligned),n.float32),
              gpuarray.empty((1,N_T_aligned),n.float32))
        gpts = gpuarray.to_gpu(pts.reshape((-1,3)).astype(n.float32))
        gI = gpuarray.to_gpu(n.identity(3,dtype=n.float32).reshape((1,9)))

        cudaworker.cukrns.slice('linear',2,gQ,gfVnopre,gpts, gI,None,1,stream=stream)

        for Rsym in Rsyms:
            cRsym = Rsym.reshape((3,3))
            Rs = n.array([cR.reshape((3,3)).dot(cRsym.dot(cR.reshape((3,3)).T))
                          for cR in offRs],dtype=n.float32)
            gRs = gpuarray.to_gpu(Rs.reshape((-1,9)).astype(n.float32))
            
            cudaworker.cukrns.slice('linear',2,gP,gfV,gpts,gRs,None,1,stream=stream)
            
            cudaworker.cukrns.shifted_squared_error(N_R, N_S, N_T, gphis.reshape((N_R*N_S)), gP, gQ,  gts, gpts, 2.0*n.pi/N, None, broadcast_Q=True, stream=stream)
            
            if stream is not None:
                stream.synchronize()

            gret += gphis

        ret = gret.get()

    return ret.reshape((N_R))

def readMRCheader (fname):
    hdr = None
    with open(fname) as f:
        hdr = {}
        header = n.fromfile(f, dtype=n.int32, count=256)
        header_f = header.view(n.float32)
        [hdr['nx'], hdr['ny'], hdr['nz'], hdr['datatype']] = header[:4]
        [hdr['xlen'],hdr['ylen'],hdr['zlen']] = header_f[10:13]
        # print "Nx %d Ny %d Nz %d Type %d" % (nx, ny, nz, datatype)
    return hdr

def readMRC (fname, inc_header=False):
    hdr = readMRCheader(fname)
    nx = hdr['nx']
    ny = hdr['ny']
    nz = hdr['nz']
    datatype = hdr['datatype']
    with open(fname) as f:
        f.seek(1024)  # seek to start of data
        if datatype == 0:
            data = n.reshape(n.fromfile(f, dtype='int8', count= nx*ny*nz), (nx,ny,nz), order='F')
        elif datatype == 1:
            data = n.reshape(n.fromfile(f, dtype='int16', count= nx*ny*nz), (nx,ny,nz), order='F')
        elif datatype == 2:
            data = n.reshape(n.fromfile(f, dtype='float32', count= nx*ny*nz), (nx,ny,nz), order='F')
        else:
            assert False,'Unsupported MRC datatype: {0}'.format(datatype)
    if inc_header:
        return data,hdr
    else:
        return data

def align_symmetry(V,symop,max_radwn= 10,verbose=0, cuda_dev=1):
	if not cudaworker.cuda_init_done: cudaworker.cuda_init(cuda_dev)
    #assert len(V.shape) == 3 
	N = V.shape[0]
    #assert all([V.shape[i]==N for i in range(3)])
	if max_radwn is None:max_radwn = N/2 - 1
	premult3 = sigproc.generate_premultiplier(N, 3)
	print('length', len(premult3))
	print(premult3.shape)
	fVnopre = fourier.fft(V).astype(n.complex64)
	fV = fourier.fft(V/premult3).astype(n.complex64)
	with cudaworker.GPUContext():
		stream = cudaworker.cudrv.Stream()
		gfV = (gpuarray.to_gpu(n.copy(fV.real).astype(n.float32)), gpuarray.to_gpu(n.copy(fV.imag).astype(n.float32)))
		gfVnopre = (gpuarray.to_gpu(n.copy(fVnopre.real).astype(n.float32)), gpuarray.to_gpu(n.copy(fVnopre.imag).astype(n.float32)))
	delta_R_thresh = 5e-2*geometry.angle_at_radwn(max_radwn)
	r_factor = 1.0/8.0
	init_r_grid = 6
	radwn = 5
	rs, dr = geometry.gen_rs(init_r_grid, symop)
	best_R = None
	for it in range(10):
		print('iter ...', it)
		radwn_ang = geometry.angle_at_radwn(radwn)
		if True:
			print 'Aligning at radwn = {0}, N_R = {1}'.format(radwn,rs.shape[0])
			print '  dr = {0}'.format(dr),
		errs = compute_symmetry_errs(rs,symop,gfV,gfVnopre,radwn,stream=stream)
		errs_best = errs.min()
		errs_best_r = errs.argmin()
		prevbest_R = best_R
		best_R = geometry.expmap(rs[errs_best_r])
		if prevbest_R is not None:
			delta_R = min([n.arccos(n.clip(0.5*(n.trace(prevbest_R.T.dot(symR.dot(best_R))) - 1),-1,1)) \
			     for symR in symop.get_rotations()])
		else:
			delta_R = n.inf
		if verbose > 0:
			print ', delta_R = {0}'.format(delta_R)
		best_thresh = (2.25 - float(radwn)/max_radwn)*errs_best
		subd_R = (delta_R >= delta_R_thresh or dr >= radwn_ang) and dr > 0.25*radwn_ang
		if subd_R:
			r_thresh = min(n.percentile(errs, 100*r_factor),best_thresh)
			rs = rs[errs <= r_thresh]
			rs, dr = geometry.subdivde(rs, dr)
		gc.collect()
		if radwn == max_radwn and ((not subd_R) or \
								   (delta_R < delta_R_thresh)):
			break
		if dr < radwn_ang:
			radwn = n.minimum(radwn + 5, 10)#max_radwn)
	return best_R, n.zeros(3)
    
    
def align_symmetryXXX(V,symop,max_radwn= 10,verbose=0, cuda_dev=0):
	if not cudaworker.cuda_init_done: cudaworker.cuda_init(cuda_dev)
	N = V.shape[0]
	if max_radwn is None:max_radwn = N/2 - 1
	premult3 = sigproc.generate_premultiplier(N, 3)
	print('length', len(premult3))
	print(premult3.shape)
	fVnopre = fourier.fft(V).astype(n.complex64)
	fV = fourier.fft(V/premult3).astype(n.complex64)
	with cudaworker.GPUContext():
		stream = cudaworker.cudrv.Stream()
		gfV = (gpuarray.to_gpu(n.copy(fV.real).astype(n.float32)), gpuarray.to_gpu(n.copy(fV.imag).astype(n.float32)))
		gfVnopre = (gpuarray.to_gpu(n.copy(fVnopre.real).astype(n.float32)), gpuarray.to_gpu(n.copy(fVnopre.imag).astype(n.float32)))
	delta_R_thresh = 5e-2*geometry.angle_at_radwn(max_radwn)
	r_factor = 1.0/8.0
	init_r_grid = 32
	radwn = 50
	rs, dr = geometry.gen_rs(init_r_grid, symop)
	best_R = None
	import time
	tic = time.time()
	for it in range(5000):
		print('iter ...', it)
		radwn_ang = geometry.angle_at_radwn(radwn)
		if True:
			print 'Aligning at radwn = {0}, N_R = {1}'.format(radwn,rs.shape[0])
			print '  dr = {0}'.format(dr),
		errs = compute_symmetry_errs(rs,symop,gfV,gfVnopre,radwn,stream=None)
		"""
		if dr>=0.13:
			errs_best   = errs.min()
			errs_best_r = errs.argmin()
			prevbest_R  = best_R
			best_R = geometry.expmap(rs[errs_best_r])
			if prevbest_R is not None:
				delta_R = min([n.arccos(n.clip(0.5*(n.trace(prevbest_R.T.dot(symR.dot(best_R))) - 1),-1,1)) \
					 for symR in symop.get_rotations()])
			else:
				delta_R = n.inf
			if verbose > 0:
				print ', delta_R = {0}'.format(delta_R)
			best_thresh = (2.25 - float(radwn)/max_radwn)*errs_best
			subd_R = (delta_R >= delta_R_thresh or dr >= radwn_ang) and dr > 0.25*radwn_ang
			if it<=3:
				if subd_R:
					r_thresh = min(n.percentile(errs, 100*r_factor),best_thresh)
					rs = rs[errs <= r_thresh]
					rs, dr = geometry.subdivde(rs, dr)
				gc.collect()
				if radwn == max_radwn and ((not subd_R) or \
										   (delta_R < delta_R_thresh)):
					break
				if dr < radwn_ang:
					radwn = n.minimum(radwn + 5, 10)#max_radwn)
		"""
	print(time.time()-tic)
	return best_R, n.zeros(3)
    
def align_symmetryEEE(V,symop,max_radwn= 10,verbose=0, cuda_dev=0):
	#if not cudaworker.cuda_init_done:
	import pycuda.gpuarray as gpuarray 
	cudaworker.cuda_init(cuda_dev)
	N = V.shape[0]
	if max_radwn is None:max_radwn = N/2 - 1
	premult3 = sigproc.generate_premultiplier(N, 3)
	print('length', len(premult3))
	print(premult3.shape)
	fVnopre = fourier.fft(V).astype(n.complex64)
	fV = fourier.fft(V/premult3).astype(n.complex64)
	with cudaworker.GPUContext():
		stream   = cudaworker.cudrv.Stream()
		gfV            = (gpuarray.to_gpu(n.copy(fV.real).astype(n.float32)), gpuarray.to_gpu(n.copy(fV.imag).astype(n.float32)))
		gfVnopre       = (gpuarray.to_gpu(n.copy(fVnopre.real).astype(n.float32)), gpuarray.to_gpu(n.copy(fVnopre.imag).astype(n.float32)))
	delta_R_thresh = 5e-2*geometry.angle_at_radwn(max_radwn)
	r_factor = 1.0/8.0
	init_r_grid = 32
	radwn = 50
	rs, dr = geometry.gen_rs(init_r_grid, symop)
	best_R = None
	import time
	tic = time.time()
	for it in range(5000):
		print('iter ...', it)
		radwn_ang = geometry.angle_at_radwn(radwn)
		if True:
			print 'Aligning at radwn = {0}, N_R = {1}'.format(radwn,rs.shape[0])
			print '  dr = {0}'.format(dr),
		errs = compute_symmetry_errs(rs,symop,gfV,gfVnopre,radwn,stream=None)
		"""
		if dr>=0.13:
			errs_best   = errs.min()
			errs_best_r = errs.argmin()
			prevbest_R  = best_R
			best_R = geometry.expmap(rs[errs_best_r])
			if prevbest_R is not None:
				delta_R = min([n.arccos(n.clip(0.5*(n.trace(prevbest_R.T.dot(symR.dot(best_R))) - 1),-1,1)) \
					 for symR in symop.get_rotations()])
			else:
				delta_R = n.inf
			if verbose > 0:
				print ', delta_R = {0}'.format(delta_R)
			best_thresh = (2.25 - float(radwn)/max_radwn)*errs_best
			subd_R = (delta_R >= delta_R_thresh or dr >= radwn_ang) and dr > 0.25*radwn_ang
			if it<=3:
				if subd_R:
					r_thresh = min(n.percentile(errs, 100*r_factor),best_thresh)
					rs = rs[errs <= r_thresh]
					rs, dr = geometry.subdivde(rs, dr)
				gc.collect()
				if radwn == max_radwn and ((not subd_R) or \
										   (delta_R < delta_R_thresh)):
					break
				if dr < radwn_ang:
					radwn = n.minimum(radwn + 5, 10)#max_radwn)
		"""
	print(time.time()-tic)/5000.
	return best_R, n.zeros(3)

    
    
import os
import symmetry
os.environ["CRYOSPARC_ROOT_DIR"] = "../runtest"
symop = symmetry.get_symmetryop('C1')
data_path_abs='../runtest/vol.mrc'
N = 256//8
map_r = readMRC(data_path_abs)
input_structure_datas = []
input_structure_datas.append(map_r)

initmodel = input_structure_datas[0]
initmodel = fourier.resample_real(initmodel, N)
align_symmetryEEE(initmodel,symop, 10, verbose=1, cuda_dev=0)
