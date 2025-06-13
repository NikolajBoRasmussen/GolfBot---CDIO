import socket
import time
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank

# Initialize hardware
gyro = GyroSensor()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

def calibrate_gyro():
    print("Calibrating gyro sensor...")
    gyro.reset()
    time.sleep(2)  # Keep robot still during this time
    print("Gyro calibration done.")

def turn_to_angle(target_angle):
    Kp = 2.0  # Proportional control gain
    threshold = 2  # degrees tolerance

    while True:
        current_angle = gyro.angle % 360
        error = (target_angle - current_angle + 540) % 360 - 180  # shortest rotation direction

        if abs(error) < threshold:
            tank_drive.off()
            break

        turn_speed = max(min(Kp * error, 50), -50)
        tank_drive.on(turn_speed, -turn_speed)
        time.sleep(0.01)

def move_robot(command):
    if command == "forward":
        tank_drive.on(SpeedPercent(30), SpeedPercent(30))
    elif command == "left":
        tank_drive.on(SpeedPercent(-20), SpeedPercent(20))
    elif command == "right":
        tank_drive.on(SpeedPercent(20), SpeedPercent(-20))
    elif command == "stop":
        tank_drive.off()
    elif command == "gyro_calibrate":
        calibrate_gyro()
    else:
        print("Unknown command: {}".format(command))

def start_server():
    HOST = ''  # Listen on all interfaces
    PORT = 9999

    calibrate_gyro()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print("Server listening on port {}...".format(PORT))

        while True:
            conn, addr = s.accept()
            with conn:
                print("Connected by {}".format(addr))
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    message = data.decode().strip()
                    print("Received: {}".format(message))

                    if message.startswith("turn:"):
                        try:
                            angle = float(message.split(":")[1])
                            print("Turning to angle: {}".format(angle))
                            turn_to_angle(angle)
                        except Exception as e:
                            print("Invalid turn command: {}".format(e))
                    else:
                        move_robot(message)

if __name__ == "__main__":
    start_server()
