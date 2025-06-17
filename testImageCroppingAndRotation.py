import cv2
import numpy as np
from ultralytics import YOLO
import cv2
import argparse
import supervision as sv
import os
import time

def get_objects(box, class_id):
    if box.cls == class_id:
        return box.xywh[0].cpu().numpy()
    return None

def get_white_balls(results):
    white_balls = []
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if box.cls == 4:  # Assuming class ID 4 is for the white balls
                    white_balls.append(box.xywh[0].cpu().numpy())  # Append the bounding box coordinates
    return white_balls

def sort_corners(corners):
    # Convert to NumPy array for vectorized operations
    corners = np.array(corners)
    
    # Sort by y-coordinate to separate top and bottom
    sorted_by_y = corners[np.argsort(corners[:, 1])]
    
    top_two = sorted_by_y[:2]
    bottom_two = sorted_by_y[2:]
    
    # Sort top two by x to get top-left, top-right
    top_left, top_right = top_two[np.argsort(top_two[:, 0])]
    
    # Sort bottom two by x to get bottom-left, bottom-right
    bottom_left, bottom_right = bottom_two[np.argsort(bottom_two[:, 0])]
    
    return [top_left, top_right, bottom_right, bottom_left]


def get_corners(results):
    corners = []
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if box.cls == 0:
                    corners.append(box.xywh[0].cpu().numpy())  # Append the bounding box coordinates
    return corners

def crop_rotate_warp(image, corners):
    # Ensure corners are sorted correctly
    corners = np.array(sort_corners(corners), dtype="float32")

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

# Example usage
model = YOLO("Models/Field Training 1/weights/best.onnx", task="detect")  # Load the trained YOLOv8 model
image = cv2.imread("field.jpg")
results = model.predict(image) # Predict on a test image
corners = get_corners(results)
corners = [[corner[0], corner[1]] for corner in corners]

cross = None
egg = None
robot = None
orange_ball = None
white_balls = None
if corners:
    transformed_image = crop_rotate_warp(image, corners)
    cv2.imwrite("Aligned-Field6.jpg", transformed_image)
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    model = YOLO("Models/New Training 1/weights/best.onnx", task="detect")  # Load the trained YOLOv8 model
    results1 = model("Aligned-Field6.jpg")[0]  # Predict on the transformed image
    plspls = model.predict("Aligned-Field6.jpg")  # Predict on the transformed image    
    detection = sv.Detections.from_yolov8(results1)
    print(type(results1), type(detection))
    print(detection.xyxy)
    frame = box_annotator.annotate(scene = transformed_image, detections = detection)
    cv2.imwrite("Aligned-Field-anno.jpg", frame)
    for result in plspls:
                for box in result.boxes:
                    match box.cls:
                        case 0:
                            if cross is not None:
                                if (cross[3] < get_objects(box, 0)[3] and cross[2] < get_objects(box, 0)[2]):
                                    cross = get_objects(box, 0)
                            else:
                                cross = get_objects(box, 0)
                            print("cross =", cross)
                        case 1:
                            if egg is not None:
                                if (egg[3] < get_objects(box, 1)[3] and egg[2] < get_objects(box, 1)[2]):
                                    egg = get_objects(box, 1)
                            else:
                                egg = get_objects(box, 1)
                            print("egg =", egg)
                        case 2:
                            orange_ball = get_objects(box, 2)
                            print("orange ball =", orange_ball)
                        case 3:
                            if robot is not None:
                                if (robot[3] < get_objects(box, 3)[3] and robot[2] < get_objects(box, 3)[2]):
                                    robot = get_objects(box, 3)
                            else:
                                robot = get_objects(box, 3)
                            print("robot =", robot)
                        case 4:
                            white_balls = get_white_balls(plspls)
    for ball in white_balls:
        print(ball)
    image = cv2.imread("Aligned-Field6.jpg")  # Load the image
    height, width, channels = image.shape  # Get dimensions

    print(f"Width: {width}, Height: {height}, Channels: {channels}")

  

    cv2.waitKey(0)
    cv2.destroyAllWindows()