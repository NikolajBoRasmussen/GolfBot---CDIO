# # main.py

import json

from ImageRecognitionModule.CameraSetup import remove_previous_images, parse_arguments, config_camera
from ImageRecognitionModule.Detecting import coord_finder
from ev3_controller import EV3Controller
from Navigation.config import GRID_SIZE
import math



def to_int_cm(pt):
    x, y = pt
    return int(round(float(x))), int(round(float(y)))


def main():
  
    # 1) Opsæt EV3-klient
    EV3_IP = "172.20.10.14"
    ev3 = EV3Controller(EV3_IP)

    caught_orange = False  # Husk om den orange bold allerede er hentet

            # 5) Udtræk koordinater (orange vs. hvide bolde)
    coords = coord_finder(caught_orange)
    if not coords:
        print("Ingen koordinater fundet, afslutter.")
    

    print("Robot:", coords[1])
    cross = coords[0]
    robot = coords[1]
    orange_ball = coords[3]
    white_balls = coords[4]

    cross_q   = to_int_cm(cross)
    robot_q   = to_int_cm(robot)
    white_qs  = [to_int_cm(pt) for pt in white_balls]
    orange_q  = to_int_cm(orange_ball) if orange_ball is not None else None

    tasks = []
    tasks.append({"name": "cross", "x": cross_q[0], "y": cross_q[1]})
    tasks.append({"name": "robot", "x": robot_q[0], "y": robot_q[1]})

    # orange hvis vi har en
    if orange_q is not None:
        tasks.append({"name": "orange", "x": orange_q[0], "y": orange_q[1]})


    white_list = [
        {"name": "white", "x": x, "y": y}
        for x, y in white_qs
    ]
    tasks.append(white_list)

    print("Gitter-koordinater og objekter:", tasks)
    ev3.send(json.dumps({"coords": tasks}))

    ack = ev3.recv()
    print("EV3 svarede:", ack)

    # 9) Opdater state, når orange bold er hentet
    if not caught_orange:
        caught_orange = True

    # 10) Stop, hvis ingen hvide bolde tilbage
    if caught_orange and not white_balls:
        print("Alle hvide bolde samlet ind – færdig.")
        exit

if __name__ == "__main__":
    main()
