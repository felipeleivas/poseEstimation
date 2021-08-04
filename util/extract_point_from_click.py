import cv2
import numpy as np
import glob
# Picture path
# img = cv2.imread('../medias/kang0.jpg')
# pixels = []
pointFilePath = 'points/pointFiles.csv'



def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        img = param['image']
        pixels = param['pixels']
        xy = '%d,%d' % (x, y)
        pixels.append([x,y])

        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow('image', img)


if __name__ == '__main__':

    for file in glob.glob('../medias/carro_2_metros0.jpg'):
        print(file)
        img = cv2.imread(file)
        filename = file.split('/')[-1]
        pixels = []
        cv2.namedWindow('image')
        params = {}
        params['image'] = img
        params['pixels'] = pixels
        cv2.setMouseCallback('image', on_EVENT_LBUTTONDOWN, params)
        cv2.imshow('image', img)
        cv2.waitKey(0)
        pointFile = open(pointFilePath, 'a')
        pointFile.write(file)
        pointFile.write(',')
        for i in range(0, len(pixels)):
            pixel = pixels[i]
            print(filename + 'p' + str(i) + ' - x: ' + str(pixel[0]) + ' y: ' + str(pixel[1]))
            pointFile.write(str(pixel[0]))
            pointFile.write(',')
            pointFile.write(str(pixel[1]))
            pointFile.write(',')
        pointFile.write('\n')
        pointFile.close()

