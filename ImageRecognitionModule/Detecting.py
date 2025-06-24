from ultralytics import YOLO
import cv2
import supervision as sv
import time
from ImageRecognitionModule.FieldDetector import find_field
from ImageRecognitionModule.CameraSetup import remove_previous_images, parse_arguments, config_camera
from ImageRecognitionModule.ResizeImage import crop_rotate_warp
from ImageRecognitionModule.ObjectSetter import set_objects

def convert_object_to_xy(cross, egg, robot, orange_ball, image_width, image_height):
    # Compute scale factors
    scale_x = 169 / image_width
    scale_y = 124.5 / image_height

    # Convert the object coordinates to real-world centimeter values
    cross = [(cross[0] * scale_x)+1, (cross[1] * scale_y)-1]
    egg = [(egg[0] * scale_x)+1, (egg[1] * scale_y)-1]
    robot = [(robot[0] * scale_x)+2, (robot[1] * scale_y)+2]
    if(orange_ball is not None):
        # Ensure orange_ball is not None before accessing its elements
        orange_ball = [(orange_ball[0] * scale_x)+1, (orange_ball[1] * scale_y)-1]
        return cross, egg, robot, orange_ball
    else:
        return cross, egg, robot

def convert_white_balls_to_xy(white_balls, image_width, image_height):
    # Compute scale factors
    scale_x = 169 / image_width
    scale_y = 124.5 / image_height

    # Convert white ball coordinates to real-world centimeter values
    white_balls = [[(ball[0] * scale_x)-1, (ball[1] * scale_y)-1] for ball in white_balls]

    return white_balls

def coord_finder(OnlyWhiteBalls):
    Sender = "Objects1" if OnlyWhiteBalls else "Objects2"
    remove_previous_images(Sender)  #fjerner tidligere billeder, så der ikke er forvirring med gamle billeder
    args = parse_arguments()
    cap = config_camera(args)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        coord_finder()

    
    ObjectModel = YOLO("Models/New Training 1/weights/best.onnx", task="detect")  # Load the trained YOLOv8 model
    
    box_annotator = sv.BoxAnnotator(
        thickness=2,
       # text_thickness=2,
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

        if not OnlyWhiteBalls:
        # Check for specific class IDs and perform actions accordingly
            if (0 in detection.class_id and crossFound != True):
                time.sleep(3)
                crossFound = True
                print("cross found")
                if (1 in detection.class_id and eggFound != True):
                    eggFound = True
                    print("egg found")
                    if (3 in detection.class_id and robotFound != True):
                        robotFound = True
                        print("robot found")
                        if (4 in detection.class_id and white_balls_found != True):
                            white_balls_found = True
                            print("white balls found")
                            if (2 in detection.class_id and orange_ball_found != True or OnlyWhiteBalls):
                                orange_ball_found = True
                                print("orange ball found")
                            else:
                                cap.release()  # Release the video capture
                                cv2.destroyAllWindows()  # Close OpenCV windows
                                return None

            if(crossFound and eggFound and robotFound and orange_ball_found and white_balls_found and not OnlyWhiteBalls):
                time.sleep(3)
                corners = find_field()
                Image = crop_rotate_warp(original_frame, corners)
                cv2.imwrite("ImageRecognitionModule/Aligned-Field.jpg", Image)
                objects = ObjectModel.predict("ImageRecognitionModule/Aligned-Field.jpg") # Predict on a test image
                cross, egg, robot, orange_ball, white_balls = set_objects(objects)

  
                if (cross is not None and egg is not None and robot is not None and orange_ball is not None and white_balls is not None):
                    cap.release()  # Release the video capture
                    cv2.destroyAllWindows()  # Close OpenCV windows
                    width, height = Image.shape[1], Image.shape[0]
                    cross, egg, robot, orange_ball = convert_object_to_xy(cross, egg, robot, orange_ball, width, height)
                    white_balls = convert_white_balls_to_xy(white_balls, width, height)
                    return cross, robot, egg, orange_ball, white_balls
                else:
                    print("Failed to find all objects. Retrying...")
                    cap.release()  # Release the video capture
                    cv2.destroyAllWindows()  # Close OpenCV windows 
                    return None
        
        if (OnlyWhiteBalls):
            
            corners = find_field()
            WhiteImage = crop_rotate_warp(original_frame, corners)
            cv2.imwrite("ImageRecognitionModule/Aligned-Field-White.jpg", WhiteImage)
            
            objects = ObjectModel.predict("ImageRecognitionModule/Aligned-Field-White.jpg")
            cross, egg, robot, orange_ball, white_balls = set_objects(objects)
            orange_ball = None
            cap.release()  # Release the video capture
            cv2.destroyAllWindows()  # Close OpenCV windows
            width, height = WhiteImage.shape[1], WhiteImage.shape[0]
            cross, egg, robot = convert_object_to_xy(cross, egg, robot, orange_ball, width, height)
            white_balls = convert_white_balls_to_xy(white_balls, width, height)
            print("White Balls:", white_balls) 
            
            return cross, robot, egg, white_balls
        
        #tryk escape for at stoppe programmet
        if(cv2.waitKey(30)==27):
            break