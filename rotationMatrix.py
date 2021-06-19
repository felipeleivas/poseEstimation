import numpy as np
import math
 
SHOULD_PRINT = False

def getRotationMatrix(alpha, beta, gama):
	cosAlpha = math.cos(alpha)
	sinAlpha = math.sin(alpha)
	cosBeta = math.cos(beta)
	sinBeta = math.sin(beta)
	cosGama = math.cos(gama)
	sinGama = math.sin(gama)

	r1 = cosAlpha * cosBeta
	r2 = (cosAlpha * sinBeta * sinGama) - (sinAlpha * cosGama)
	r3 = (cosAlpha * sinBeta * cosGama) + (sinAlpha * sinGama)
	r4 = sinAlpha * cosBeta
	r5 = (sinAlpha * sinBeta * sinGama) + (cosAlpha * cosGama)
	r6 = (sinAlpha * sinBeta * cosGama) + (cosAlpha * sinGama)
	r7 = -sinBeta
	r8 = cosBeta * sinGama
	r9 = cosBeta * cosGama


	rotationMatrix = np.array([[r1,r2,r3], [r4,r5,r6], [r7,r8,r9]])
	# print(rotationMatrix)

	# print(np.cross(np.array([r1,r4,r7]), np.array([r2,r5,r8]) ))
	return rotationMatrix