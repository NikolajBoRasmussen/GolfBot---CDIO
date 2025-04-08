from roboflow import Roboflow

#Hvis alt går syd, så anvender vi labelIMG i stedet.

rf = Roboflow(api_key= "RMNjWAs5Y6ZLzs9MI8uF")
list_of_workspaces = rf.workspace()
print(list_of_workspaces)
project = rf.workspace().project("golfbot-fyxfe")
dataset = project.version(2).download("yolov8")
