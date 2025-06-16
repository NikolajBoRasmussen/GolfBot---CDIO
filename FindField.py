from ultralytics import YOLO
import cv2
import argparse
import supervision as sv
import os
import time
import numpy as np

#def construct_sides_from_corners(corners):
    # Ensure corners is a list of 4 points
#    if len(corners) != 4:
#        raise ValueError("Need exactly 4 corner points to construct sides.")
    
#    sides = []
#    for i in range(4):
#        start_point = corners[i]
#        end_point = corners[(i + 1) % 4]  # Wrap around for last point
#        sides.append((start_point.tolist(), end_point.tolist()))
    
#    return sides

def is_point_inside_polygon(corners, point):
    polygon = np.array(corners, dtype=np.float32)

    # Use OpenCV's pointPolygonTest
    return cv2.pointPolygonTest(polygon, tuple(point), False) >= 0

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

def remove_previous_images():
    file_path = "Field.jpg"

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

def find_field():
    remove_previous_images()  #fjerner tidligere billeder, så der ikke er forvirring med gamle billeder
    args = parse_arguments()
    cap = config_camera(args)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        find_field()

    
    model = YOLO("Models/Field Training 1/weights/best.onnx", task="detect")  # Load the trained YOLOv8 model
    
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
        
        if 0 in detection.class_id:  # Check if the field is detected
            cv2.imwrite("field.jpg", original_frame)
            cv2.imwrite("fieldtest.jpg", frame)
            results = model.predict("field.jpg") # Predict on a test image
            corners = get_corners(results)
            if corners:

                corners = sort_corners(corners)
                corners = [[corner[0], corner[1]] for corner in corners]
                for corner in corners:
                    print("Field corners:", corner)
                #object_position = [66, 300]
                #print("Object inside field:", is_point_inside_polygon(corners, object_position))
                
                return corners
                #sides = construct_sides_from_corners(corners)
                #print("Field sides:", sides)        

        
        #tryk escape for at stoppe programmet
        if(cv2.waitKey(30)==27):
            break
        
        
        
if __name__ == "__main__":
    find_field()