import cv2
from src.camera import getPixelPointFromRealWorldCordinates

BLUE = (255., 0., 0.)
GREEN = (0., 255., 0.)
RED = (0., 0., 255.)
BLACK = (0., 0., 0.)
WHITE = (255., 255., 255.)


def draw_plates(pixels, K, R, T, image, coordinates):
    drawRectangle(pixels, RED, image)
    newPixels = []
    for coordinate in coordinates:
        newPixels.append(getPixelPointFromRealWorldCordinates(K, R, T, coordinate))
    drawRectangle(newPixels, BLUE, image)


def drawRectangle(points, color, image):
    for i in range(0, len(points)):
        pt1 = roundPoint(points[i]);
        pt2 = roundPoint(points[(i + 1) % len(points)]);
        cv2.line(image, tuple(pt1), tuple(pt2), color, 2)


def roundPoint(point):
    x = int(point[0] + 0.5)
    y = int(point[1] + 0.5)

    return (x, y)


def draw_circle(x, y, img, color):
    xy = '%d,%d' % (x, y)
    cv2.circle(img, (x, y), 1, color, thickness=-1)
    cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, color , thickness=1)


def draw_circles(pixels, img, color):
    for pixel in pixels:
        x, y = pixel
        draw_circle(x, y, img, color)
