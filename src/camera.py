import numpy as np

def getPixelPointFromRealWorldCordinates(K,R,T, coordinate):
	point = coordinate.copy()
	point = np.append(point, 1)
	rt= np.concatenate((R,T),1)
	A = np.dot(K,rt)

	pixelVector = np.dot(A, np.array(point))
	pixelVector = [pixelVector[0]/pixelVector[2], pixelVector[1]/pixelVector[2]]
	return pixelVector