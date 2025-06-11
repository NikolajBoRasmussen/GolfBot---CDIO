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


#Load pretrained Yolov8 model from YOLOv8 repo
model = YOLO('yolov8n.pt', task = "detect")    #yolov8n.pt might be better
#model2 = YOLO('yolov8n-seg.pt')  # Load a pretrained YOLOv8 model
#model3 = YOLO('yolov8n-eval.pt')  # Load a pretrained YOLOv8 model for evaluation
#model4 = YOLO('yolov8n-seg-eval.pt')  # Load a pretrained YOLOv8 model for segmentation evaluation


model.info()     #kan være brugbar til debugging


#Train the model
model.train(data='GolfBot-9/data.yaml', epochs=100, batch=12, project = "Models", name = "New Training 1")

# Evaluation of the model
results = model.val() # Evaluate the model on the validation set
#results2 = model2.val() # Evaluate the segmentation model on the validation set

results1 = model.predict("test.jpg") # Predict on a test image

# Export the model to ONNX format
model.export(format='onnx')
model.save("yolov8n.pt")