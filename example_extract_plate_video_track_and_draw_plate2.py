import glob

import torch
import os
import plate_detectation.example_plate_detection as plate_detection
from calculate_speed import get_speed_from_content
from calibration import getMatrix
from src.configuration.configuration import get_matrix
from src.util.draw import draw_plates, drawRectangle, BLUE, GREEN
from src.util.video import create_output_video_writer
from util import *
import numpy as np
import pytesseract


if __name__ == '__main__':
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
    model.classes = [2]
    model.conf = 0.4

    K = get_matrix('camera.calibration', (3, 3), float)
    coordinates = get_matrix('license.plate.coordinates', (4, 3), float)
    csv_filename_original = 'csv/speed_file'
    csv_filename = csv_filename_original
    i = 1
    while os.path.exists(csv_filename + '.csv'):
        csv_filename = csv_filename_original + str(i)
        i+=1
    csv = open(csv_filename + '.csv', 'w')

    for videoPath in glob.glob('videos/01_08/hb20_68.mp4'):
        print('Parsing video: ' + videoPath)
        imagePath = videoPath[0: videoPath.rfind('.')]
        imageFilename = imagePath[videoPath.find('/'): ]

        video = cv2.VideoCapture(videoPath)
        video_out = create_output_video_writer(video, 'output/' + imageFilename + '.mp4', 3)
        points_file = open('points/' + imageFilename + '.csv', 'w')

        index = 0

        points_str = ''
        while (video.isOpened()):
            # Capture frame-by-frame
            ret, originalImage = video.read()
            if ret == True:
                image = originalImage.copy()
                results = model(image)
                pixels = []
                for x in results.xyxy[0]:
                    xmin = int(x[0].numpy())
                    ymin = int(x[1].numpy())
                    xmax = int(x[2].numpy())
                    ymax = int(x[3].numpy())
                    points = [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]
                    drawRectangle(points, GREEN, image)
                    crop_img = image[ymin:ymax, xmin:xmax]
                    detectedPixels = plate_detection.get_lp_points_from_image(crop_img)
                    if detectedPixels is not None:
                        for pixel in detectedPixels:
                            pixel[0] = pixel[0] + xmin
                            pixel[1] = pixel[1] + ymin

                        pixels.append(detectedPixels)

                if len(pixels) > 0:
                    for pixel in pixels :
                        R, T = getMatrix(K, pixel, coordinates)
                        draw_plates(pixel, K, R, T, image, coordinates)
                        timestamp = video.get(cv2.CAP_PROP_POS_MSEC)
                        if timestamp > 0.0:
                            points_str += str(timestamp) + ',' + str(T[0][0]) + ',' + str(T[1][0]) + ',' + str(T[2][0]) + '\n'
                        xmin = len(image[0])
                        xmax = 0
                        ymin = len(image)
                        ymax = 0
                        for pixelCord in pixel:
                            xCord = int(pixelCord[0])
                            yCord = int(pixelCord[1])

                            if xCord > xmax:
                                xmax = xCord
                            if xCord < xmin:
                                xmin = xCord
                            if yCord < ymin:
                                ymin = yCord
                            if yCord > ymax:
                                ymax = yCord

                        # gray = cv2.cvtColor(originalImage[ymin:ymax, xmin:xmax], cv2.COLOR_RGB2GRAY)
                        # gray, img_bin = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                        # gray = cv2.bitwise_not(img_bin)
                        # kernel = np.ones((2, 1), np.uint8)
                        # # img = cv2.erode(gray, kernel, iterations=1)
                        # # img = cv2.dilate(img, kernel, iterations=1)
                        # out_below = pytesseract.image_to_string(gray)
                        # print("OUTPUT:", out_below)
                        cv2.imwrite("plates/" + imageFilename + str(index) + ".png", originalImage[ymin:ymax, xmin:xmax])
                        # cv2.imshow("teste2", gray)
                        # cv2.waitKey(0)
                        index += 1
                video_out.write(image)

            # Break the loop
            else:
                velocity = imageFilename[imageFilename.rfind('_') + 1::]
                average, median, fmean = get_speed_from_content(points_str)
                csv.write(imageFilename + ';' + velocity + ';' + str(average) + ';' + str(median) + ';' + str(fmean) + '\n')
                points_file.write(points_str)
                break

        points_file.close()
        video_out.release()
    csv.close()
