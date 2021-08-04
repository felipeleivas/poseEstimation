import cv2

import plate_detectation.example_plate_detection as plate_detection
from calibration import getMatrix
from camera import K, getPixelPointFromRealWorldCordinates
from util import *

coordinates = [[0, 0, 0], [0.4, 0, 0], [0.4, .13, 0], [0, .13, 0]]

if __name__ == '__main__':

    videoPath = 'videos/hb20_30_cutted_output.mp4'
    cap = cv2.VideoCapture(videoPath)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # Check if camera opened successfully

    imagePath = videoPath.split('.')[0]
    index = 0
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    out = cv2.VideoWriter(imagePath + '_output.mp4', fourcc, fps, (1920, 1080))

    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, image = cap.read()
        if ret == True:
            pixels = plate_detection.get_lp_points_from_image(image)
            if pixels != None:
                R, T = getMatrix(K, pixels, coordinates)
                drawRectangle(pixels, RED, image)
                newPixels = []

                for coordinate in coordinates:
                    newPixels.append(getPixelPointFromRealWorldCordinates(K, R, T, coordinate))

                drawRectangle(newPixels, BLUE, image)
            out.write(image)
        # Break the loop
        else:
            break
    out.release()
    cv2.waitKey(0)
