import numpy as np
arr = np.full((10, 10, 10), 0.0, dtype=np.float32)
farr = np.fft.fftn(arr)
print(farr.shape)
for i in range(farr.shape[0]):
	for j in range(farr.shape[1]):
		for k in range(farr.shape[2]//2+1):
			farr[i][j][k] =    complex(i+j+k, i+j+k+5.)
			farr[i][j][k+4] =  complex(i+j+k, -(i+j+k+5.))
			
			
arr1 = np.fft.ifftn(farr)
#print(arr1)
for i in range(arr1.shape[0]):
	for j in range(arr1.shape[1]):
		for k in range(arr1.shape[2]):
			if abs(arr1[i][j][k].real) >0.00001:
				print(arr1[i][j][k])
			else:
				print(0.0, 0.0)
exit()

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