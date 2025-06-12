from ultralytics import YOLO
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import argparse
import supervision as sv
import os
import time
    
def get_cross(results):
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if box.cls == 0:
                    return box.xywh[0].cpu().numpy()
    return None

def get_robot(results):
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if box.cls == 3:  # Assuming class ID 1 is for the robot
                    return box.xywh[0].cpu().numpy()  # Return the bounding box coordinates
    return None

def get_egg(results):
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if box.cls == 1:  # Assuming class ID 1 is for the egg
                    return box.xywh[0].cpu().numpy()  # Return the bounding box coordinates
    return None

def get_white_balls(results):
    white_balls = []
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if box.cls == 4:  # Assuming class ID 4 is for the white balls
                    white_balls.append(box.xywh[0].cpu().numpy())  # Append the bounding box coordinates
    return white_balls

def get_orange_ball(results):
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if box.cls == 2:  # Assuming class ID 2 is for the orange ball
                    return box.xywh[0].cpu().numpy()  # Return the bounding box coordinates
    return None


def remove_previous_images():
    file_path = "yolov8.jpg"

    # Check if the file exists before trying to remove it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been removed.")
    else:
        print(f"{file_path} does not exist.")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description= "YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution",
        default= [640, 640],
        nargs = 2,
        type=int
    )
    args = parser.parse_args()
    return args

def config_camera(args: argparse.Namespace):
    frame_width, frame_height = args.webcam_resolution
    
    #print(cv2.getBuildInformation())
    #nedenstående funktion tænder kameraet i index 1. Indexet starter på 0, men for mig der er kameraet i index 0 mit kamera i min pc.
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    return cap

def main():
    remove_previous_images()  #fjerner tidligere billeder, så der ikke er forvirring med gamle billeder
    args = parse_arguments()
    cap = config_camera(args)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    
    model = YOLO("Models/New Training 1/weights/best.onnx", task="detect")  # Load the trained YOLOv8 model
    
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    
    crossFound = False
    eggFound = False
    robotFound = False
    white_balls_found = False
    
    while True:
        ret, frame = cap.read()
        
        original_frame = frame.copy()
        result = model(frame)[0]
        detection = sv.Detections.from_yolov8(result)
        frame = box_annotator.annotate(scene = frame, detections = detection)
        
        cv2.imshow("yolov8", frame)
        
        print(detection.class_id)
        #print(detection.xyxy)
        #print(detection.confidence)
                
        if(0 in detection.class_id and crossFound != True):
            time.sleep(3)
            cv2.imwrite("yolov8cross.jpg", original_frame)
            cv2.imwrite("yolov8testcross.jpg", frame)
            results1 = model.predict("yolov8cross.jpg") # Predict on a test image            
            cross = get_cross(results1)
            crossFound = True
            print("cross = ", cross)
        
        if (1 in detection.class_id and eggFound != True and crossFound == True):
            time.sleep(3)
            cv2.imwrite("yolov8egg.jpg", original_frame)
            cv2.imwrite("yolov8testegg.jpg", frame)
            results1 = model.predict("yolov8egg.jpg") # Predict on a test image
            egg = get_egg(results1)
            eggFound = True
            print("egg = ", egg)
        
        if (3 in detection.class_id and robotFound != True and crossFound == True and eggFound == True):
            time.sleep(3)
            cv2.imwrite("yolov8robot.jpg", original_frame)
            cv2.imwrite("yolov8testrobot.jpg", frame)
            results1 = model.predict("yolov8robot.jpg") # Predict on a test image
            robot = get_robot(results1)
            robotFound = True
            print("robot = ", robot)
            
        if (2 in detection.class_id and crossFound == True and eggFound == True and robotFound == True and white_balls_found == True):
            time.sleep(3)
            cv2.imwrite("yolov8.jpg", original_frame)
            cv2.imwrite("yolov8test.jpg", frame)
            results1 = model.predict("yolov8.jpg") # Predict on a test image            
            print(results1[0].boxes.xywh)
            orange_ball = get_orange_ball(results1)
            print(orange_ball)
            break
        
        if (4 in detection.class_id and white_balls_found != True and crossFound == True and eggFound == True and robotFound == True):
            white_balls_found = True
            time.sleep(3)
            cv2.imwrite("yolov8whiteballs.jpg", original_frame)
            cv2.imwrite("yolov8testwhiteballs.jpg", frame)
            results1 = model.predict("yolov8whiteballs.jpg")
            white_balls = get_white_balls(results1)
            print("white balls = ", white_balls)
        #tryk escape for at stoppe programmet
        if(cv2.waitKey(30)==27):
            break
    
if __name__ == "__main__":
    main()