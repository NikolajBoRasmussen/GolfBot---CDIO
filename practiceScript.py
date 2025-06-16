from ultralytics import YOLO
import cv2
import argparse
import time
import supervision as sv
# Importér EV3Controller fra classen i ev3_controller.py
from ev3_controller import EV3Controller  

# Henter objekter fra YOLOv8 resultater baseret på klasse ID
def get_objects_by_class(results, class_id):
    coords = []
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if int(box.cls) == class_id:
                    coords.append(box.xywh[0].cpu().numpy())
    return coords

# Parser webcam opløsning fra argumenter
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--webcam-resolution", default=[640, 640], nargs=2, type=int)
    return parser.parse_args()

# Konfigurerer kameraet
def config_camera(args: argparse.Namespace):
    cap = cv2.VideoCapture(0)  # Brug index 0 eller index 1 afhængigt af dit system.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.webcam_resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.webcam_resolution[1])
    return cap

# Main program
def main():
    args = parse_arguments()
    cap = config_camera(args)
    model = YOLO("Models/New Training 13/weights/best.onnx", task="detect")
    box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)

    # Opret forbindelse til robotten (Indtast IP-adresse for EV3 nedenunder)
    ev3 = EV3Controller("172.20.10.14")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Kunne ikke læse fra kameraet")
                break

            result = model(frame)[0]
            detection = sv.Detections.from_yolov8(result)
            frame = box_annotator.annotate(scene=frame, detections=detection)

            # Annoterede objekter i billedet - 4=hvide bolde, 3=robot
            balls = get_objects_by_class([result], 4)
            robot = get_objects_by_class([result], 3)

            # Så længe der er både bolde og robot i billedet, send nedenstående kommandoer til EV3
            if balls and robot:
                ev3.send("forward")
                ev3.send("left")
                ev3.send("forward")
                ev3.send("right")
                ev3.send("forward")
                ev3.send("stop")

            cv2.imshow("YOLOv8", frame)

            # ESC for at afslutte
            if cv2.waitKey(1) == 27:
                ev3.send("stop")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        ev3.close()  # Luk forbindelsen til EV3

if __name__ == "__main__":
    main()
