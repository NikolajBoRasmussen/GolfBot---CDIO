from roboflow import Roboflow

#Hvis alt går syd, så anvender vi labelIMG i stedet.

rf = Roboflow(api_key= "RMNjWAs5Y6ZLzs9MI8uF") #format =, skal måske bruges
list_of_workspaces = rf.workspace()
project = rf.workspace().project("golfbot-fyxfe")
dataset = project.version(8).download("yolov8") #yolov8-obb skal måske bruges
