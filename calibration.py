from scipy import linalg
import numpy as np

SHOULD_PRINT = False
def getMatrix(K,pixels, coordinates):
	kInv = np.linalg.inv(K)
	A = []
	y = []
	for i in range(0, len(pixels)):
		pixel = [pixels[i][0], pixels[i][1], 1]
		coordinate = coordinates[i]
		A.append([coordinate[0],coordinate[1], 1, 0,0,0,0,0,0])
		A.append([0,0,0, coordinate[0],coordinate[1], 1,0,0,0])
		A.append([ 0,0,0,0,0,0,coordinate[0],coordinate[1], 1])
		kInvPixel = np.dot(kInv,pixel)
		y.append([kInvPixel[0]])
		y.append([kInvPixel[1]])
		y.append([kInvPixel[2]])
	A = np.array(A)
	y = np.array(y)

	AT = np.transpose(A)

	A = np.dot(AT, A)
	y = np.dot(AT, y)

	system = np.linalg.solve(A,y)

	r1 = np.array([system[0][0], system[3][0], system[6][0]])
	r2 = np.array([system[1][0], system[4][0], system[7][0]])
	moduleR1 = np.linalg.norm(r1)
	moduleR2 = np.linalg.norm(r2)
	avgModule = (moduleR2 + moduleR1)/2
	r1 = r1/moduleR1
	r2 = r2/moduleR2

	r3 = np.cross(r1,r2)

	t = np.array([system[2],system[5],system[8]])/avgModule
	R = np.array([
			[r1[0],r2[0],r3[0]],
			[r1[1],r2[1],r3[1]],
			[r1[2],r2[2],r3[2]]
	])
	T = np.array([
	t[0],
	t[1],
	t[2]
	])

	return R,T