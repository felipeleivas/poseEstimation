import glob

from calibration import getMatrix
from src.configuration.configuration import get_matrix
from src.pixels import get_pixels_right_order
from src.util.draw import draw_plates, draw_circles, BLACK, GREEN
from src.util import SPACE_BAR, ESC
from src.util.video import create_output_video_writer
from util import *


def on_EVENT_LBUTTONDOWN(event, x, y, _, pixels):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixels.append([x, y])
    if event == cv2.EVENT_MBUTTONDOWN:
        if len(pixels) > 0:
            pixels.pop()


if __name__ == '__main__':
    K = get_matrix('camera.calibration', (3, 3), float)
    coordinates = get_pixels_right_order(get_matrix('license.plate.coordinates', (4, 3), float))
    should_quit = False

    for videoPath in glob.glob('videos/01_08/*.mp4'):
        if should_quit:
            break
        imagePath = videoPath[0: videoPath.rfind('.')]
        imageFilename = imagePath[videoPath.rfind('/')::]
        print('Parsing video: ' + imageFilename)

        video = cv2.VideoCapture(videoPath)
        video_out = create_output_video_writer(video, 'output/' + imageFilename + '.mp4', 3)
        points_file = open('points/' + imageFilename + '_manual.csv', 'a')
        points_file.write('begin - attempt: \n')
        index = 0
        play_video = True
        pixels = []
        init = True
        delay = 20
        written_line = ''
        while video.isOpened() and not should_quit:

            if play_video:
                ret, original_image = video.read()
                if init:
                    cv2.waitKey(0)
                init = False
            if ret == True:
                image = original_image.copy()
                cv2.imshow('image', image)
                cv2.setMouseCallback('image', on_EVENT_LBUTTONDOWN, pixels)
                draw_circles(pixels, image, GREEN)
                cv2.imshow('image', image)

            pressed_key = cv2.waitKey(delay) & 0xFF

            if pressed_key == SPACE_BAR:
                if not play_video and len(pixels) == 4:
                    pixels = get_pixels_right_order(pixels)
                    R, T = getMatrix(K, pixels, coordinates)
                    draw_plates(pixels, K, R, T, image, coordinates)
                    timestamp = video.get(cv2.CAP_PROP_POS_MSEC)
                    written_line += str(timestamp) + ',' + str(T[0][0]) + ',' + str(T[1][0]) + ',' + str(T[2][0]) + '\n'
                    pixels = []
                    cv2.imshow('image', image)
                    cv2.waitKey(0)
                play_video = not play_video
                delay *= 2
            if pressed_key == ord('s'):
                delay *= 2
                if delay > 100000:
                    delay = 100000
            if pressed_key == ord('a'):
                delay = int(delay/2)
                if delay < 1:
                    delay = 1

            if pressed_key == ESC or pressed_key == ord('q'):
                should_quit = True
            if pressed_key == ord('r'):
                video = cv2.VideoCapture(videoPath)
                pixels = []
                delay = 20
                written_line = ''
            if pressed_key == ord('n'):
                break

        points_file.write(written_line + 'end - attempt: \n\n ')
        points_file.close()
        video_out.release()
