from roboflow import Roboflow

rf = Roboflow(api_key= "RMNjWAs5Y6ZLzs9MI8uF") #format =, skal måske bruges
workspace  = rf.workspace()
project = rf.workspace().project("find-the-field")
dataset = project.version(2).download("yolov8") #yolov8-obb skal måske bruges