from ultralytics import YOLO
import cv2
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
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    
    model = YOLO("Models/New Training 1/weights/best.onnx")
    
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    
    while True:
        ret, frame = cap.read()
        
        # Draw a blue rectangle (BGR: Blue=(255, 0, 0))
        #Rectangle begin
        top_left = (65, 52)
        #rectangle end
        bottom_right = (575, 427)
        #Rectangle color
        color = (255, 0, 0)  # Blue in BGR
        thickness = 2
        # Draw the rectangle on the frame
        cv2.rectangle(frame, top_left, bottom_right, color, thickness)
        
        # Inference and annotation
        result = model(frame)[0]
        detection = sv.Detections.from_yolov8(result)
        frame = box_annotator.annotate(scene=frame, detections=detection)

        # Show the frame
        cv2.imshow("yolov8", frame)

        print(detection)

        if cv2.waitKey(30) == 27:
            break

    
if __name__ == "__main__":
    main()