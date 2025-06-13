from ultralytics import YOLO
import cv2
import math
import socket
import supervision as sv
import argparse
import time

def calculate_angle_to_ball(ball_x, ball_y, robot_x, robot_y):
    dx = ball_x - robot_x
    dy = ball_y - robot_y
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    if angle_deg < 0:
        angle_deg += 360
    return angle_deg

def send_command_to_ev3(command):
    EV3_IP = "172.20.10.3"  # Replace with your EV3's IP
    PORT = 9999
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((EV3_IP, PORT))
            s.sendall(command.encode())
    except Exception as e:
        print("Failed to send command to EV3:", e)

def get_objects_by_class(results, class_id):
    coords = []
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if int(box.cls) == class_id:
                    coords.append(box.xywh[0].cpu().numpy())
    return coords

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--webcam-resolution", default=[640, 640], nargs=2, type=int)
    return parser.parse_args()

def config_camera(args: argparse.Namespace):
    cap = cv2.VideoCapture(0)  # Use correct index or backend if needed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.webcam_resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.webcam_resolution[1])
    return cap

def main():
    args = parse_arguments()
    cap = config_camera(args)
    model = YOLO("Models/New Training 13/weights/best.onnx", task="detect")
    box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)

    last_command = ""
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Only process every 2nd frame to improve performance
        if frame_count % 2 == 0:
            result = model(frame)[0]
            detection = sv.Detections.from_yolov8(result)
            frame = box_annotator.annotate(scene=frame, detections=detection)

            balls = get_objects_by_class([result], 4)  # Class 4: ball
            robots = get_objects_by_class([result], 3)  # Class 3: robot

            if balls and robots:
                ball_x, ball_y, _, _ = balls[0]
                robot_x, robot_y, _, _ = robots[0]

                desired_angle = calculate_angle_to_ball(ball_x, ball_y, robot_x, robot_y)
                command = f"turn:{desired_angle}"

                if command != last_command:
                    print(f"Sending turn command: {command}")
                    send_command_to_ev3(command)
                    last_command = command

                dx = ball_x - robot_x
                dy = ball_y - robot_y
                distance = math.sqrt(dx**2 + dy**2)
                STOP_THRESHOLD = 50

                if distance > STOP_THRESHOLD:
                    command = "forward"
                else:
                    command = "stop"

                if command != last_command:
                    print(f"Sending move command: {command}")
                    send_command_to_ev3(command)
                    last_command = command

            else:
                # Robot or ball not visible
                command = "stop"
                if command != last_command:
                    print("Robot or ball lost. Stopping.")
                    send_command_to_ev3(command)
                    last_command = command

        # Show the frame regardless of whether we ran detection
        cv2.imshow("YOLOv8", frame)
        if cv2.waitKey(1) == 27:  # ESC to exit
            send_command_to_ev3("stop")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
