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

def coord_finder(OnlyWhiteBalls):
    remove_previous_images()  #fjerner tidligere billeder, så der ikke er forvirring med gamle billeder
    args = parse_arguments()
    cap = config_camera(args)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        coord_finder()

    
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
    orange_ball_found = False
    cross = None
    egg = None
    robot = None
    orange_ball = None
    white_balls = None
    
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

        # Check for specific class IDs and perform actions accordingly
        if (0 in detection.class_id and crossFound != True):
            time.sleep(3)
            cv2.imwrite("yolov8cross.jpg", original_frame)
            cv2.imwrite("yolov8testcross.jpg", frame)
            results1 = model.predict("yolov8cross.jpg") # Predict on a test image
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
            cv2.imwrite("yolov8.jpg", original_frame)
            cv2.imwrite("yolov8test.jpg", frame)
            results1 = model.predict("yolov8.jpg") # Predict on a test image
            for result in results1:
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
                            white_balls = get_white_balls(results1)
                            print("white balls =", white_balls)

  
            print("Tjekpoint")
            if (cross is not None and egg is not None and robot is not None and orange_ball is not None and white_balls is not None):
                print("cross = ", cross)
                print("egg = ", egg)
                print("robot = ", robot)
                print("orange ball = ", orange_ball)
                print("white balls = ", white_balls)
                return cross, robot, egg, orange_ball, white_balls
        
        if (OnlyWhiteBalls):
            if (crossFound and eggFound and robotFound and white_balls_found):
                cv2.imwrite("yolov8cross.jpg", original_frame)
                cv2.imwrite("yolov8testcross.jpg", frame)
                results1 = model.predict("yolov8cross.jpg")
                white_balls = get_white_balls(results1)
                return white_balls
        
        #tryk escape for at stoppe programmet
        if(cv2.waitKey(30)==27):
            break