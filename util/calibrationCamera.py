import numpy as np
import cv2
import glob
import os

if __name__ == '__main__':
    path = os.getcwd()
    images = []
    # print(path)
    cap = cv2.VideoCapture('videos/calibracao.mp4')
    i = 0
    images = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        # if(i%50 == 0):
        images.append(frame)
        # cv2.imwrite('medias/kang'+str(i)+'.jpg',frame)
        # print(i)
        i += 1

    cap.release()
    print(len(images))

    # cv2.destroyAllWindows()
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    # images = glob.glob('*.jpg')
    for fname in images:
        img = fname
        # img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

    cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    print('ret -> ', ret)
    print('mtx -> ', mtx)

# print('dist -> ' , dist )
# print('rvecs -> ' , rvecs )
# print('tvecs -> ' , tvecs )
