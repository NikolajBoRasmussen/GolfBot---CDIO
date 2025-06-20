# # main.py

# import time
# import json
# import cv2
# import argparse

# from ultralytics import YOLO
# import supervision as sv

# from ImageRecognitionModule.CameraSetup import remove_previous_images, parse_arguments, config_camera
# from ImageRecognitionModule.Detecting    import coord_finder
# from ev3_controller                      import EV3Controller
# from Navigation.config                   import GRID_SIZE
# import math

# def quantize_point(point):
#     x, y = point
#     gs   = GRID_SIZE
#     return (math.floor(x/gs) * gs,
#             math.floor(y/gs) * gs)

# def main():
#     # 0) Opsæt kamera-loop som før
#     args  = parse_arguments()                     # kun webcam-resolution
#     cap   = config_camera(args)                   # bruger din CameraSetup.config_camera
#     model = YOLO("Models/New Training 1/weights/best.onnx")  
#     box_annotator = sv.BoxAnnotator(thickness=2, text_scale=1)

#     # 1) Opsæt EV3-client
#     EV3_IP = "172.20.10.10"  
#     ev3    = EV3Controller(EV3_IP)

#     caught_orange = False

#     try:
#         while True:
#             # ——— live‐detection (præcis som før) ———
#             ret, frame = cap.read()
#             if not ret:
#                 print("Kamera gav ikke frame – stopper.")
#                 break

#             result     = model(frame)[0]
#             detections = sv.Detections.from_yolov8(result)
#             annotated  = box_annotator.annotate(scene=frame, detections=detections)

#             cv2.imshow("YOLOv8 Live", annotated)
#             print(detections)

#             # ESC for at bryde ud af live‐loopet
#             if cv2.waitKey(30) == 27:
#                 break

#         # ——— efter ESC: hent coords og kør runflow ———
#         remove_previous_images("Field")
#         cv2.imwrite("ImageRecognitionModule/field.jpg", frame)  # gem sidste frame
#         coords = coord_finder(caught_orange)
#         if not coords:
#             print("Ingen koordinater fundet, afslutter.")
#             return

#         orange_ball = coords[3]
#         white_balls = coords[4]
#         if not caught_orange:
#             tasks = [orange_ball]
#         else:
#             tasks = white_balls

#         # Kvantiser
#         tasks = [quantize_point(pt) for pt in tasks]
#         print("Gitter-koordinater:", tasks)

#         # Send til EV3
#         ev3.send(json.dumps({"coords": tasks}))
#         print("EV3 svarede:", ev3.recv())

#     finally:
#         cap.release()
#         ev3.close()
#         cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()


# main.py

import time
import json
import cv2
import argparse

from ultralytics import YOLO
import supervision as sv

from ImageRecognitionModule.CameraSetup import remove_previous_images, parse_arguments, config_camera
from ImageRecognitionModule.Detecting import coord_finder
from ev3_controller import EV3Controller
from Navigation.config import GRID_SIZE
import math

def quantize_point(point):
    """Kvantisér et punkt til nærmeste grid-koordinat."""
    x, y = point
    gs = GRID_SIZE
    return (math.floor(x/gs) * gs,
            math.floor(y/gs) * gs)

def main():
    # 0) Opsæt kamera
    args = parse_arguments()                 # Indlæs evt. kommandolinje-argumenter for webcam
    cap = config_camera(args)                # Initialiser kamera med de givne parametre
    model = YOLO("Models/New Training 1/weights/best.onnx")  # Indlæs dit trænete YOLO-model
    box_annotator = sv.BoxAnnotator(thickness=2, text_scale=1)

    # 1) Opsæt EV3-klient
    EV3_IP = "172.20.10.10"
    ev3 = EV3Controller(EV3_IP)

    caught_orange = False  # Husk om den orange bold allerede er hentet

    try:
        while True:
            # 2) Tag et billede fra kameraet
            ret, frame = cap.read()
            if not ret:
                print("Kamera gav ikke frame – stopper.")
                break

            # 3) (Valgfrit) Vis live-annoteret billede
            result = model(frame)[0]
            detections = sv.Detections.from_yolov8(result)
            annotated = box_annotator.annotate(scene=frame, detections=detections)
            cv2.imshow("YOLOv8 Live", annotated)

            # 4) Ryd gamle billeder og gem ny til koordinatudtræk
            remove_previous_images("Field")
            cv2.imwrite("ImageRecognitionModule/field.jpg", frame)

            # 5) Udtræk koordinater (orange vs. hvide bolde)
            coords = coord_finder(caught_orange)
            if not coords:
                print("Ingen koordinater fundet, afslutter.")
                break

            orange_ball = coords[3]
            white_balls = coords[4]

            # 6) Vælg tasks: orange først, dernæst alle hvide
            if not caught_orange:
                tasks = [orange_ball]
            else:
                tasks = white_balls

            # 7) Kvantiser alle valgte punkter
            tasks = [quantize_point(pt) for pt in tasks]
            print("Gitter-koordinater:", tasks)

            # 8) Send til EV3 og vent på ack
            ev3.send(json.dumps({"coords": tasks}))
            ack = ev3.recv()
            print("EV3 svarede:", ack)

            # 9) Opdater state, når orange bold er hentet
            if not caught_orange:
                caught_orange = True

            # 10) Stop, hvis ingen hvide bolde tilbage
            if caught_orange and not white_balls:
                print("Alle hvide bolde samlet ind – færdig.")
                break

            # 11) Kort pause før næste iteration
            time.sleep(0.5)

            # 12) Manuel afslutning (ESC)
            if cv2.waitKey(1) == 27:
                print("Bruger afbrød med ESC.")
                break
    finally:
        cap.release()
        ev3.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
