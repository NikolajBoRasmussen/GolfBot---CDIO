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

#Test balls 
model = YOLO('Models/Training 24/weights/best.onnx', task = "detect")

results1 = model.predict("test.jpg") # Predict on a test image

print(results1)
