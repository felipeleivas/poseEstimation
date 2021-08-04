import glob

import plate_detectation.example_plate_detection as plate_detection
from calibration import getMatrix
from src.configuration.configuration import get_matrix
from src.util.draw import draw_plates
from src.util.video import create_output_video_writer
from util import *
import torch


if __name__ == '__main__':
    K = get_matrix('camera.calibration', (3, 3), float)
    coordinates = get_matrix('license.plate.coordinates', (4, 3), float)

    for videoPath in glob.glob('videos/*_cutted_output.mp4'):
        print('Parsing video: ' + videoPath)
        imagePath = videoPath[0: videoPath.rfind('.')]
        imageFilename = imagePath[videoPath.rfind('/'): -1]

        video = cv2.VideoCapture(videoPath)
        video_out = create_output_video_writer(video, 'output/' + imageFilename + '.mp4', 3)
        points_file = open('points/' + imageFilename + '.csv', 'w')

        index = 0

        while (video.isOpened()):
            # Capture frame-by-frame
            ret, image = video.read()
            if ret == True:

                pixels = plate_detection.get_lp_points_from_image(image)

                if pixels != None:
                    R, T = getMatrix(K, pixels, coordinates)
                    draw_plates(pixels, K, R, T, image, coordinates)
                    timestamp = video.get(cv2.CAP_PROP_POS_MSEC)
                    points_file.write(
                        str(timestamp) + ',' + str(T[0][0]) + ',' + str(T[1][0]) + ',' + str(T[2][0]) + '\n')
                video_out.write(image)
            # Break the loop
            else:
                break
        points_file.close()
        video_out.release()
