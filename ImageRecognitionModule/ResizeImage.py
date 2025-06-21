import cv2
import numpy as np

def crop_rotate_warp(image, corners):
    # Ensure corners are sorted correctly
    corners = np.array(corners, dtype="float32")

    # Compute width & height using Euclidean distance
    width = int(max(np.linalg.norm(corners[0] - corners[1]), np.linalg.norm(corners[2] - corners[3])))
    height = int(max(np.linalg.norm(corners[0] - corners[3]), np.linalg.norm(corners[1] - corners[2])))

    # Compute the rotation angle using the top-left to top-right edge
    dx = corners[1][0] - corners[0][0]
    dy = corners[1][1] - corners[0][1]
    angle = np.degrees(np.arctan2(dy, dx))

    center = tuple(np.mean(corners, axis=0)[:2])  # Extract only x and y values
    # Compute the rotation matrix
    M_rot = cv2.getRotationMatrix2D(center, -angle, 1.0)

    # Apply rotation correction
    rotated_image = cv2.warpAffine(image, M_rot, (image.shape[1], image.shape[0]))

    # Define destination points for perspective correction
    dst_pts = np.array([
        [0, 0], [width, 0], [width, height], [0, height]
    ], dtype="float32")

    # Compute transformation matrix
    M_persp = cv2.getPerspectiveTransform(corners, dst_pts)

    # Apply perspective warp
    warped_image = cv2.warpPerspective(rotated_image, M_persp, (width, height))

    return warped_image