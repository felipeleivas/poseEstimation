import numpy as np
from math import pi
from rotationMatrix import getRotationMatrix


SHOULD_PRINT = False
ALPHA = pi/2
BETA = 0
GAMA = 0

K = np.array([
    [1711.50988, 0.00000000, 590.733223],
    [0.00000000, 1702.53509, 995.529274],
    [0.00000000, 0.00000000, 1.00]
])
R = getRotationMatrix(ALPHA, BETA, GAMA)
T = np.array([[1.7],[-8],[1.5]])


