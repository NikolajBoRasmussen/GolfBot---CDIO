from ultralytics import YOLO
import cv2
import argparse
import supervision as sv
import os
import time
import TestCameraCapture as tcc
from TestCameraCapture import coord_finder

def retrieve_coordinates():
    coords = coord_finder()  # Call the function to get coordinates

    if coords:  # Check if cords is not None
        print("Cross:", coords[0])
        print("Robot:", coords[1])
        print("Egg:", coords[2])
        print("Orange Ball:", coords[3])

        print("White Ball Coordinates:")
        for ball in coords[4]:  # Assuming cords[4] holds multiple white balls
            print(ball)
        exit
    else:
        print("Failed to retrieve coordinates.")

if __name__ == "__main__":
    retrieve_coordinates()