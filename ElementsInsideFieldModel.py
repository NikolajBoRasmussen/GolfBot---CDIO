from ultralytics import YOLO

#Load pretrained Yolov8 model from YOLOv8 repo
model = YOLO('yolov8n.pt', task = "detect")    #yolov8n.pt might be better
#model2 = YOLO('yolov8n-seg.pt')  # Load a pretrained YOLOv8 model
#model3 = YOLO('yolov8n-eval.pt')  # Load a pretrained YOLOv8 model for evaluation
#model4 = YOLO('yolov8n-seg-eval.pt')  # Load a pretrained YOLOv8 model for segmentation evaluation


model.info()     #kan være brugbar til debugging


#Train the model
model.train(data='GolfBot-9/data.yaml', epochs=150, batch=16, project = "Models", name = "New Training 1")

# Evaluation of the model
results = model.val() # Evaluate the model on the validation set
#results2 = model2.val() # Evaluate the segmentation model on the validation set

results1 = model.predict("test.jpg") # Predict on a test image

# Export the model to ONNX format
model.export(format='onnx')
model.save("yolov8n.pt")