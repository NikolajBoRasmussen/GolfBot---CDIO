from ultralytics import YOLO
import cv2
import argparse
import supervision as sv
import os
import time
import numpy as np

def compute_scaling(corners, object):
    width_pixel = abs(corners[1][0] - corners[0][0])  # Top-right to top-left distance
    height_pixel = abs(corners[2][1] - corners[0][1])  # Bottom-left to top-left distance
    
    scale_x = 169 / width_pixel  # cm per pixel for X
    scale_y = 124.5 / height_pixel  # cm per pixel for Y
    
    obj_x_cm = (object[0] - corners[0][0]) * scale_x  # Distance from left boundary
    obj_y_cm = (object[1] - corners[0][1]) * scale_y  # Distance from top boundary
    
    if(is_point_inside_polygon())
        return [obj_x_cm, obj_y_cm]
    

def is_point_inside_polygon(corners, point):
    polygon = np.array(corners, dtype=np.float32)

    # Use OpenCV's pointPolygonTest
    return cv2.pointPolygonTest(polygon, tuple(point), False) >= 0