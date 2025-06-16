from ultralytics import YOLO
import cv2
import argparse
import supervision as sv
import os
import time
import TestCameraCapture as tcc
from TestCameraCapture import coord_finder
from FindField import find_field

def retrieve_coordinates():
    field = find_field()
    print("corners = ",  field)
    caught_orange_ball = False  # Initialize the flag for orange ball
    coords = coord_finder(caught_orange_ball)  # Call the function to get coordinates
    
    

    if coords:  # Check if cords is not None
        print("Cross:", coords[0])
        print("Robot:", coords[1])
        print("Egg:", coords[2])
        print("Orange Ball:", coords[3])

        print("White Ball Coordinates:")
        for ball in coords[4]:  # Assuming cords[4] holds multiple white balls
            print(ball)
        caught_orange_ball = True  # Set the flag to True if orange ball is found
        
        #kode for navigation her
    else:
        print("Failed to retrieve coordinates.")
        retrieve_coordinates()

    #hvis den kun skal finde hvide bolde
    if caught_orange_ball:
        white_balls = coord_finder(caught_orange_ball)  # Call the function again to find white balls
        if white_balls:
            print("White Ball Coordinates:")
            for ball in white_balls[4]:
                print(ball)
                
if __name__ == "__main__":
    retrieve_coordinates()