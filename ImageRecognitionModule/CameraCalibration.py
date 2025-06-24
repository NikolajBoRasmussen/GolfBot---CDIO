import numpy as np
import cv2 as cv
import glob

def calibrate_camera():
    chessboard_size = (9, 7)  # Number of inner corners per a chessboard row and column
    # Note: This is the number of inner corners, not the number of squares.
    frameSize = (640, 480)  # Size of the images used for calibration
 
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboard_size[0],0:chessboard_size[1]].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
 
    images = glob.glob('CalibrationImages/*.jpg')

    if not images:
        raise FileNotFoundError("No .jpg images found in the 'CalibrationImages' directory for calibration.")

    for image in images:
        img = cv.imread(image)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
 
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, chessboard_size, None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
 
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)
 
            # Draw and display the corners
            cv.drawChessboardCorners(img, (chessboard_size[0],chessboard_size[1]), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
 
    cv.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    img = cv.imread('left12.jpg')
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
 
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite('calibresult.png', dst)

    # Hvis første metode ikke virker, kan du prøve at bruge initUndistortRectifyMap
    # undistort
    #mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    #dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
 
    # crop the image
    #x, y, w, h = roi
    #dst = dst[y:y+h, x:x+w]
    #cv.imwrite('calibresult.png', dst)

    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error
 
    print( "total error: {}".format(mean_error/len(objpoints)) )