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
model = YOLO('yolov8n.yaml')    #yolov8n.pt might be better

#Train the model
model.train(data='data.yaml', epochs=10, batch=16, imgsz=640, device='0')

# Evaluation of the model
results = model.val()

# Export the model to ONNX format
model.export(format='onnx')