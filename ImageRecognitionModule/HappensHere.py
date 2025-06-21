from ultralytics import YOLO
import cv2
import argparse
import supervision as sv
import os
import time
from ImageRecognitionModule.Detecting import coord_finder

def retrieve_coordinates():
    caught_orange_ball = False  # Initialize the flag for orange ball
    coords = coord_finder(caught_orange_ball)  # Call the function to get coordinates
    
    if coords:  # Check if cords is not None
        print("Cross:", coords[0])
        cross = coords[0]  # Store the cross coordinates

        print("Robot:", coords[1])
        robot = coords[1]
        
        print("Egg:", coords[2])
        egg = coords[2]
        
        print("Orange Ball:", coords[3])
        orange_ball = coords[3]

        print("White Ball Coordinates:")
        white_balls = coords[4]
        for ball in white_balls:  # Assuming cords[4] holds multiple white balls
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
        for ball in coords[4]:
            print(ball)
        
        for ball in white_balls:
            print(ball)

                
if __name__ == "__main__":
    retrieve_coordinates()