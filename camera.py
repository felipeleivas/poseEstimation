import numpy as np
from math import pi
from rotationMatrix import getRotationMatrix


SHOULD_PRINT = False
ALPHA = pi/2
BETA = 0
GAMA = 0 

K = np.array([[1,0,0], [0,1,0], [0,0,1/64]])
R = getRotationMatrix(ALPHA, BETA, GAMA)
T = np.array([[1],[1],[1]])


def getPixelPointFromRealWorldCordinates(K,R,T, point):
	point.append(1)
	rt= np.concatenate((R,T),1)
	A = np.dot(K,rt)

	pixelVector = np.dot(A, np.array(point) )
	pixelVector = [pixelVector[0]/pixelVector[2], pixelVector[1]/pixelVector[2]]
	return pixelVector