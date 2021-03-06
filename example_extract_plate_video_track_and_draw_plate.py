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

    for videoPath in glob.glob('videos/01_08/*.mp4'):
        print('Parsing video: ' + videoPath)
        imagePath = videoPath[0: videoPath.rfind('.')]
        imageFilename = imagePath[videoPath.find('/'): ]

        video = cv2.VideoCapture(videoPath)
        fps = video.get(cv2.CAP_PROP_FPS)
        video_out = create_output_video_writer(video, 'output/' + imageFilename + '.mp4', 3)
        points_file = open('points/' + imageFilename + '.csv', 'w')

        index = 0

        points_str = ''
        while (video.isOpened()):
            # Capture frame-by-frame
            ret, image = video.read()
            if ret == True:
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
                        # if 15 > T[2][0] > 6:
                        draw_plates(pixel, K, R, T, image, coordinates)
                        timestamp = video.get(cv2.CAP_PROP_POS_FRAMES) * fps
                        points_str += str(timestamp) + ',' + str(T[0][0]) + ',' + str(T[1][0]) + ',' + str(T[2][0]) + '\n'
                        # if timestamp > 0.0:

                video_out.write(image)

            # Break the loop
            else:
                points_file.write(points_str)
                velocity = imageFilename[imageFilename.rfind('_') + 1::]
                average, median, fmean, _ = get_speed_from_content(points_str)
                print('imageFilename: ',imageFilename)
                print('avarage: ', average, 'median: ', median, 'fmean:', fmean)
                csv.write(imageFilename + ';' + velocity + ';' + str(average) + ';' + str(median) + ';' + str(fmean) + '\n')
                break

        points_file.close()
        video_out.release()
    csv.close()
