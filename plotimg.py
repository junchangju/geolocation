#!/usr/bin/env python 

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


filename = sys.argv[1]
corr = np.loadtxt(filename)
plt.imshow(corr, cmap='gray', interpolation='nearest')
plt.title(filename)
plt.clim(0.92,1.0)
plt.show()
quit()

scorr = np.sort(corr, axis=None)[::-1]
N = 8
row0,col0 = np.where(scorr[0] == corr)
if len(row0) != 1:
	print filename, ": max not unique"
	exit

good = True
for i in np.arange(1,N):
	row,col = np.where(scorr[i] == corr)
	if len(row) != 1:
		print filename, ":row is not unique"
		continue 

	if np.abs(row - row0) > 2 or np.abs(col - col0) > 2: 
		good = False
		#print "not adjacent to the max:", row, col
		break

	if (scorr[0] - scorr[i])/scorr[0] < 0.01:
		good = False
		print filename, "not steep enough:", row, col
		break

if good:
	print filename, "max:", row0, col0
	plt.imshow(corr, cmap='gray', interpolation='nearest')
	plt.title(sys.argv[1])
	plt.show()


