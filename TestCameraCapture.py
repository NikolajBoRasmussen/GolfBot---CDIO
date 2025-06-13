from ultralytics import YOLO
import cv2
import argparse
import supervision as sv
import os
import time
    

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
    cap = cv2.VideoCapture(1)
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

    
    model = YOLO("Models/Training 24/weights/best.onnx", task="detect")  # Load the trained YOLOv8 model
    
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    
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
        
        if (2 in detection.class_id):
            print("calibrating...")
            time.sleep(3)
            cv2.imwrite("yolov8.jpg", original_frame)
            cv2.imwrite("yolov8test.jpg", frame)
            results1 = model.predict("yolov8.jpg") # Predict on a test image            
            print(results1[0].boxes.xywh)
            orange_ball = get_orange_ball(results1)
            print(orange_ball)
            print("det virker")
            break
        #tryk escape for at stoppe programmet
        if(cv2.waitKey(30)==27):
            break
    
if __name__ == "__main__":
    main()