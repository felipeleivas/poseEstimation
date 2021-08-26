import glob

import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
plt.style.use('seaborn-whitegrid')

if __name__ == '__main__':

	for filepath in glob.glob('points/01_08/*[!manual].csv'):
		file = open(filepath)
		print('reading for file ' + filepath)
		content = file.read()
		i = 0
		xdata = []
		ydata = []
		zdata = []
		cdata = []
		xRot = 0
		yRot = 0
		for line in content.split('\n'):
			# print (line)
			tokens = line.split(',')
			if len(tokens) >= 4:
				xdata.append(float(tokens[0]))
				ydata.append(float(tokens[2]))
				zdata.append(float(tokens[3]))
				cdata.append(float(i))
				i += 1
		xdata = np.array(xdata)
		ydata = np.array(ydata)
		zdata = np.array(zdata)

		fig = plt.figure()
		ax = plt.axes(projection='3d')
		ax.scatter3D(xdata, ydata, zdata, cmap='Greens');

		ax.set_xlabel('Timestamp')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')

		plt.savefig('teste.png')
		plt.show()
		cv2.waitKey(0)