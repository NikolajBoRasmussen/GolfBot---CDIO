from roboflow import Roboflow

rf = Roboflow(api_key=)
project = rf.workspace().project()
dataset = project.version(2).download("yolov8")
