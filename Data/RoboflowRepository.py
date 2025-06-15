from roboflow import Roboflow

rf = Roboflow(api_key= "RMNjWAs5Y6ZLzs9MI8uF") #format =, skal måske bruges
list_of_workspaces = rf.workspace()
project = rf.workspace().project("golfbot-fyxfe")
dataset = project.version(9).download("yolov8") #yolov8-obb skal måske bruges
