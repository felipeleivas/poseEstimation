import plate_detectation.example_plate_detection as test
from calibration import getMatrix
from camera import K, getPixelPointFromRealWorldCordinates

SHOULD_PRINT = True
coordinates = [[0, 0, 0], [0.4, 0, 0], [0.4, .13, 0], [0, .13, 0]]
if __name__ == '__main__':
    # pixels = test.getLPPoints("medias/kang0.jpg")
    pixels = [[658,325],[1040,320],[1045,435],[658,439]]
    print("\n\n\n\n\n")

    print("Extracted points:")
    for pixel in pixels:
        print(pixel)

    # coordinates = [[0, 0, 0], [0.4, 0, 0], [0.4, .13, 0], [0, .13, 0]]

    R, T = getMatrix(K, pixels, coordinates)

    newPixels = []

    for coordinate in coordinates:
        newPixels.append(getPixelPointFromRealWorldCordinates(K, R, T, coordinate))


    if SHOULD_PRINT:
        print("Recalculated points:")
        for pixel in newPixels:
            print(pixel)
        print("R ->", R)
        print("T ->", T)


