import cv2

from util import *

coordinates = [[0, 0, 0], [0.4, 0, 0], [0.4, .13, 0], [0, .13, 0]]
should_write = False

def read_plate_pixels(filename):
    file = open('points/pointFiles.csv', 'r')
    pixels = []
    for line in file:
        tokens = line.replace('\n', '').split(',')
        if tokens[0] == filename:
            for index in range(1, len(tokens) - 1, 2):
                pixels.append([float(tokens[index]), float(tokens[index + 1])])
            break
    return pixels


if __name__ == '__main__':

    videoPath = '../videos/onix_70.mp4'
    cap = cv2.VideoCapture(videoPath)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # Check if camera opened successfully

    imagePath = videoPath[0: videoPath.rfind('.')]
    index = 0
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    out = cv2.VideoWriter(imagePath + '_cutted_output.mp4', fourcc, fps, (1920, 1080))

    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, image = cap.read()
        if ret == True:

            cv2.imshow('Frame', image)

            if should_write:
                out.write(image)
            if cv2.waitKey(20) & 0xFF == 32:
                should_write = True

        # Break the loop
        else:
            break
    out.release()
    # cv2.waitKey(0)
