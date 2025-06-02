from ultralytics import YOLO
import torch
import os
import shutil
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import json
import time
import copy
import glob
import sys
import cv2

def main():
    #print(cv2.getBuildInformation())
    #nedenstående funktion tænder kameraet i index 1. Indexet starter på 0, men for mig der er kameraet i index 0 mit kamera i min pc.
    cap = cv2.VideoCapture(1)
    
    while True:
        ret, frame = cap.read()
        cv2.imshow("yolov8", frame)
        
        #tryk escape for at stoppe programmet
        if(cv2.waitKey(30)==27):
            break
    
if __name__ == "__main__":
    main()