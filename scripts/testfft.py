import numpy as np
arr = np.full((15,10), 0.0, dtype=np.float32)
for i in range(arr.shape[0]):
	for j in range(arr.shape[1]):
		arr[i][j] = i+j
farr = np.fft.fft2(arr)
nc = 0
for i in range(farr.shape[0]):
	for j in range(farr.shape[1]//2+1):
		print (nc, round(np.real(farr[i][j]),9), round(np.imag(farr[i][j]),9))
		nc +=1
print(farr.shape)