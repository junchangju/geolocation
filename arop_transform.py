#!/usr/bin/env python 

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# July 10, 2020

## baserow basecol targetrow targetcol
filename = sys.argv[1]
tp = np.loadtxt(filename)
nrow = tp.shape[0]
A = np.concatenate((np.ones((nrow,1)), tp[:,[0,1]]), axis = 1)

### rows
y = tp[:,2]
coeff = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(y)
print coeff
prow = A.dot(coeff)
plt.plot(prow, y, '*')
plt.show()

### cols
y = tp[:,3]
coeff = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(y)
print coeff
pcol = A.dot(coeff)
plt.plot(pcol, y, '*')
plt.show()




