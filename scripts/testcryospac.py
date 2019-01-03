import numpy as n
"""
	maxdr = 2.0/(max_radwn) # less than half a fourier coefficient spacing
    num_iter_r = int(n.ceil(1 + n.log2((2*n.pi/init_r_grid)/maxdr))) # auto tune
    num_iter_radwn = 1 + int(n.ceil(n.exp(n.log(float(max_radwn)/init_radwn)/radwn_factor)))
    num_iter = max(num_iter_r, num_iter_radwn)
    radwn = init_radwn
    r_factor = 1.0/8.0/radwn_factor/accel_factor
    t_factor = 1.0/4.0/radwn_factor
	N_D = len(images)
	rs, dr = geometry.gen_rs(init_r_grid, symop)
    init_t_extent_pix = int(n.round(init_t_extent * N))
    ts, dt = geometry.gen_ts(init_t_grid, init_t_extent_pix)
    rss = [rs for _ in range(N_D)]
    tss = [ts for _ in range(N_D)]
"""
init_r_grid  = 20
init_radwn   = 12
radwn_factor = 1.5 
N = 384
max_radwn = None
if max_radwn is None:
	max_radwn = N/2 - 2
maxdr = 2.0/(max_radwn)
num_iter_r = int(n.ceil(1 + n.log2((2*n.pi/init_r_grid)/maxdr))) # auto tune
num_iter_radwn = 1 + int(n.ceil(n.exp(n.log(float(max_radwn)/init_radwn)/radwn_factor)))
num_iter = max(num_iter_r, num_iter_radwn)
print('num_iter_r', num_iter_r)
print('num_iter', num_iter)
print('num_iter_radwn', num_iter_radwn)

# 64: num_iter_r  4
# 384: num_iter_r 6