from ultralytics import YOLO
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import argparse
import supervision as sv

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

def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution
    
    #print(cv2.getBuildInformation())
    #nedenstående funktion tænder kameraet i index 1. Indexet starter på 0, men for mig der er kameraet i index 0 mit kamera i min pc.
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    
    model = YOLO("Models/Training 24/weights/best.onnx")
    
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    
    while True:
        ret, frame = cap.read()
        
        result = model(frame)[0]
        detection = sv.Detections.from_yolov8(result)
        frame = box_annotator.annotate(scene = frame, detections = detection)
        
        
        cv2.imshow("yolov8", frame)
        
        print(detection.class_id)
        print(detection)
        
        if (2 in detection.class_id):
            cv2.imwrite("yolov8.jpg", frame)
            results1 = model.predict("yolov8.jpg") # Predict on a test image
            print(results1)
            print("det virker")
            break
        #tryk escape for at stoppe programmet
        if(cv2.waitKey(30)==27):
            break
    
if __name__ == "__main__":
    main()