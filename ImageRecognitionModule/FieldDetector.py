from ultralytics import YOLO
import cv2
import supervision as sv
import numpy as np
from ImageRecognitionModule.CameraSetup import remove_previous_images, parse_arguments, config_camera


def is_point_inside_polygon(corners, point):
    polygon = np.array(corners, dtype=np.float32)

    # Use OpenCV's pointPolygonTest
    return cv2.pointPolygonTest(polygon, tuple(point), False) >= 0

def sort_corners(corners):
    # Convert to NumPy array for vectorized operations
    corners = np.array(corners)
    
    if len(corners) == 5:
        print("5 hjørner")
        # Compute the centroid of all points.
        centroid = np.mean(corners, axis=0)
        # Calculate the Euclidean distance from each point to the centroid.
        distances = np.linalg.norm(corners - centroid, axis=1)
        # Identify the index of the most central point.
        extra_index = np.argmin(distances)
        # Remove the extra point.
        corners = np.delete(corners, extra_index, axis=0)
    
    # Ensure that we have exactly 4 corners at this point.
    if len(corners) != 4:
        raise ValueError(f"Expected 4 corners after removal, got {len(corners)}.")

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

def find_field():
    Sender = "Field"
    remove_previous_images(Sender)  #fjerner tidligere billeder, så der ikke er forvirring med gamle billeder
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
        
        if 0 in detection.class_id:  # Check if the field is detected
            cv2.imwrite("ImageRecognitionModule/field.jpg", original_frame)
            results = model.predict("ImageRecognitionModule/field.jpg") # Predict on a test image
            corners = get_corners(results)
            if corners:

                corners = sort_corners(corners)
                corners = [[corner[0], corner[1]] for corner in corners]
                for corner in corners:
                    print("Field corners:", corner)
                cap.release()  # Release the video capture
                cv2.destroyAllWindows()  # Close OpenCV windows                
                return corners
        if(cv2.waitKey(30)==27):
            break                
        
if __name__ == "__main__":
    find_field()