#!/usr/bin/env python 

### July 10, 2020
### Trying to understand AROP. 
##  Analyse the cross-correlation between two image chips. The base
##  image chip stays fixed but the target image chip shifts around the 
##  presumed tie point by up to 15 pixels in each direction, so we get a
##  31 x 31 matrix of correlation for a potential pair of tie points.

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

filename = sys.argv[1]
corr = np.loadtxt(filename)
#   plt.imshow(corr, cmap='gray', interpolation='nearest')
#   plt.title(filename)
#   plt.show()
#   quit()

scorr = np.sort(corr, axis=None)[::-1]
rowmax,colmax = np.where(scorr[0] == corr)
if len(rowmax) != 1:
	print filename, ": max not unique"
	quit()

if scorr[0] < 0.95:
	print filename, ": max is not big enough"
	quit()

if (scorr[0] - np.mean(scorr))/np.std(scorr) < 3.5:
	print filename, ": max is not outstanding"
	quit()

# 25 points will be used to fit bivariate polynomial.
# Expect steep decline away from the pixel of max correlation.
if (scorr[0] - scorr[24])/scorr[0] < 0.2:
	good = False
	print filename, "not steep enough:"

good = True
N = 8
for i in np.arange(1,N):
	row,col = np.where(scorr[i] == corr)
	if len(row) != 1:
		good = False
		print filename, ":row is not unique"
		print row, col
		continue 

	# Expect the 8 neighbors around the max pixel to have
	# the next 8 values after the max. But it seems that some of
	# the next 8 greatest is possessed not by immediate neighbors,
	# i.e., location difference is 1.
	if np.abs(row - rowmax) > 2 or np.abs(col - colmax) > 2: 
		good = False
		#print "not adjacent to the max:", row, col
		break

if not good:
	quit()


print filename, "max:", rowmax, colmax
# plt.imshow(corr, cmap='gray', interpolation='nearest')
# plt.title(sys.argv[1])
# plt.show()


# Create correlation surface around the max correlation. Totally 5 x 5 pixels.
# Python is a lot like C; great.
#
# rowmax and colmax can't be too close to be maxtrix boundary --
# rowmax-D/2 >= 0 and colmax-D/2 >= 0
D = 5
A = np.zeros((D*D, 6), dtype=float)
y = np.zeros((D*D, 1), dtype=float)
if rowmax-D/2 < 0 or colmax-D/2 < 0 or \
   rowmax+D/2 > corr.shape[0] or colmax+D/2 > corr.shape[1]:
	quit()
for i in np.arange(0, D):
	for j in np.arange(0, D):
		y[i*D+j] = corr[rowmax-D/2+i, colmax-D/2+j] 
		A[i*D+j, 0] = 1
		A[i*D+j, 1] = i
		A[i*D+j, 2] = j
		A[i*D+j, 3] = i*i
		A[i*D+j, 4] = i*j
		A[i*D+j, 5] = j*j

#print y
#print A
C = np.linalg.inv(np.transpose(A).dot(A)).dot(np.transpose(A)).dot(y)
print C
# July 10, 2020: Confirmed by Feng that there is no coefficient 2 before squared c4.
# subrow = (C[2]*C[4] - 2*C[1]*C[5])/(4*C[3]*C[5] - 2*C[4]*C[4])
# subcol = (C[1]*C[4] - 2*C[2]*C[3])/(4*C[3]*C[5] - 2*C[4]*C[4])
subrow = (C[2]*C[4] - 2*C[1]*C[5])/(4*C[3]*C[5] - C[4]*C[4])
subcol = (C[1]*C[4] - 2*C[2]*C[3])/(4*C[3]*C[5] - C[4]*C[4])
#
# subrow and subcol is 1x1 array
maxsubrow = rowmax-D/2 + subrow[0]
maxsubcol = colmax-D/2 + subcol[0]
print subrow, subcol
#print maxsubrow, maxsubcol

# The pixel in the base image.
# Example filename: 1004.1086.1366.base.txt
str = filename.split(".")
bcol = float(str[1]); 	# In ENVI col/row order
brow = float(str[2]);

# The corresponding row/col in the target image.
# corr is square
trow = brow - corr.shape[0]/2 + maxsubrow
tcol = bcol - corr.shape[0]/2 + maxsubcol

print "final", brow,bcol,trow,tcol 
