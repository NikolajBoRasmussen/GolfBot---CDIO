import cv2
import argparse
import os


def remove_previous_images(WhoThere):
    file_path = ""
    
    if WhoThere == "Field":
        file_path = "ImageRecognitionModule/field.jpg"
    elif WhoThere == "Objects1":
        file_path = "ImageRecognitionModule/Aligned-Field-White.jpg"
    elif WhoThere == "Objects2":
        file_path = "ImageRecognitionModule/Aligned-Field.jpg"

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