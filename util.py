import random
interaval = 0
def noisePixels(pixels):
	noisePixels = []
	for pixel in pixels:
		noisePixel = []
		for coord in pixel:
			noisedCoord = random.uniform(-interaval,interaval) + coord
			noisePixel.append(noisedCoord)
		noisePixels.append(noisePixel)
	return noisePixels