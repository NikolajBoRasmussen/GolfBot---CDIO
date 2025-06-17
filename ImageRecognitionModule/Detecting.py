from ultralytics import YOLO
import cv2
import argparse
import supervision as sv
import os
import time
from FieldDetector import find_field
from CameraSetup import remove_previous_images, parse_arguments, config_camera
from ObjectGetter import get_objects, get_white_balls
from ResizeImage import crop_rotate_warp


def coord_finder(OnlyWhiteBalls):
    Sender = "Objects"
    remove_previous_images(Sender)  #fjerner tidligere billeder, så der ikke er forvirring med gamle billeder
    args = parse_arguments()
    cap = config_camera(args)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        coord_finder()

    
    ObjectModel = YOLO("Models/New Training 1/weights/best.onnx", task="detect")  # Load the trained YOLOv8 model
    
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    
    crossFound = False
    eggFound = False
    robotFound = False
    white_balls_found = False
    orange_ball_found = False
    cross = None
    egg = None
    robot = None
    orange_ball = None
    white_balls = None
    
    while True:
        ret, frame = cap.read()
        
        original_frame = frame.copy()
        result = ObjectModel(frame)[0]
        detection = sv.Detections.from_yolov8(result)
        frame = box_annotator.annotate(scene = frame, detections = detection)
                
        print(detection.class_id)
        #print(detection.xyxy)
        #print(detection.confidence)

        # Check for specific class IDs and perform actions accordingly
        if (0 in detection.class_id and crossFound != True):
            time.sleep(3)
            corners = find_field()
            Image = crop_rotate_warp(original_frame, corners)
            cv2.imwrite("ImageRecognitionModule/Aligned-Field.jpg", Image)
            crossFound = True
            print("cross found")
            if (1 in detection.class_id and eggFound != True):
                eggFound = True
                print("egg found")
                if (3 in detection.class_id and robotFound != True):
                    robotFound = True
                    print("robot found")
                    if (2 in detection.class_id and orange_ball_found != True or OnlyWhiteBalls):
                        orange_ball_found = True
                        print("orange ball found")
                        if (4 in detection.class_id and white_balls_found != True):
                            white_balls_found = True
                            print("white balls found")
        
        if(crossFound and eggFound and robotFound and orange_ball_found and white_balls_found and not OnlyWhiteBalls):
            time.sleep(3)
            corners = find_field()
            Image = crop_rotate_warp(original_frame, corners)
            cv2.imwrite("ImageRecognitionModule/Aligned-Field.jpg", Image)
            objects = ObjectModel.predict("ImageRecognitionModule/Aligned-Field.jpg") # Predict on a test image
            for object in objects:
                for box in object.boxes:
                    match box.cls:
                        case 0:
                            if cross is not None:
                                if (cross[3] < get_objects(box, 0)[3] and cross[2] < get_objects(box, 0)[2]):
                                    cross = get_objects(box, 0)
                            else:
                                cross = get_objects(box, 0)
                        case 1:
                            if egg is not None:
                                if (egg[3] < get_objects(box, 1)[3] and egg[2] < get_objects(box, 1)[2]):
                                    egg = get_objects(box, 1)
                            else:
                                egg = get_objects(box, 1)
                        case 2:
                            orange_ball = get_objects(box, 2)
                        case 3:
                            if robot is not None:
                                if (robot[3] < get_objects(box, 3)[3] and robot[2] < get_objects(box, 3)[2]):
                                    robot = get_objects(box, 3)
                            else:
                                robot = get_objects(box, 3)
                        case 4:
                            white_balls = get_white_balls(objects)

  
            print("Tjekpoint")
            if (cross is not None and egg is not None and robot is not None and orange_ball is not None and white_balls is not None):
                print("cross = ", cross)
                print("egg = ", egg)
                print("robot = ", robot)
                print("orange ball = ", orange_ball)
                print("white balls = ", white_balls)
                cap.release()  # Release the video capture
                cv2.destroyAllWindows()  # Close OpenCV windows 
                return cross, robot, egg, orange_ball, white_balls
            else:
                print("Failed to find all objects. Retrying...")
                cap.release()  # Release the video capture
                cv2.destroyAllWindows()  # Close OpenCV windows 
                coord_finder(OnlyWhiteBalls = False)
        
        if (OnlyWhiteBalls):
            if (crossFound and eggFound and robotFound and white_balls_found):
                corners = find_field()
                WhiteImage = crop_rotate_warp(original_frame, corners)
                cv2.imwrite("ImageRecognitionModule/Aligned-Field-White.jpg", WhiteImage)
                results1 = ObjectModel.predict("ImageRecognitionModule/Aligned-Field-White.jpg")
                white_balls = get_white_balls(results1)
                cap.release()  # Release the video capture
                cv2.destroyAllWindows()  # Close OpenCV windows 
                return white_balls
        
        #tryk escape for at stoppe programmet
        if(cv2.waitKey(30)==27):
            break