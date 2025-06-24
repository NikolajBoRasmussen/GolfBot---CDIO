## main.py
import json
import time
from ImageRecognitionModule.CameraSetup import remove_previous_images, parse_arguments, config_camera
from ImageRecognitionModule.Detecting import coord_finder
from ev3_controller import EV3Controller
from Navigation.config import GRID_SIZE
import math



def to_int_cm(pt):
    x, y = pt
    return int(round(float(x))), int(round(float(y)))

# Niko
# def main():
#     EV3_IP = "172.20.10.10" #Jaw
#    # EV3_IP = "172.20.10.3" #Louise
#     caught_orange = False  # Husk om den orange bold allerede er hentet
    
#     if not caught_orange or caught_orange and white_balls:
#     # 1) Find alle koordinater (én gang)
#         coords = coord_finder(caught_orange)
#         if not coords:
#             print("Ingen koordinater fundet, afslutter.")
#             return

#         cross      = coords[0]
#         robot_pos  = coords[1]
#         orange_ball= coords[3]
#         white_balls= coords[4]

#         # 2) Konverter til grid‐celler
#         cross_q   = to_int_cm(cross)
#         robot_q   = to_int_cm(robot_pos)
#         white_qs  = [to_int_cm(pt) for pt in white_balls]
#         orange_q  = to_int_cm(orange_ball) if orange_ball is not None else None

#         # 3) Byg task‐liste
#         tasks = [
#             {"name": "cross",  "x": cross_q[0],  "y": cross_q[1]},
#             {"name": "robot",  "x": robot_q[0],  "y": robot_q[1]},
#         ]
#         if orange_q is not None:
#             tasks.append({"name": "orange", "x": orange_q[0], "y": orange_q[1]})
#         else:
#             caught_orange = True  # Hvis ingen orange bold, så markeret som fanget
#         tasks.append([{"name": "white", "x": x, "y": y} for x, y in white_qs])

#         print("Gitter-koordinater og objekter:", tasks)

#         # 4) Opret EV3-forbindelse
#         ev3 = EV3Controller(EV3_IP)

#         # 5) Send og modtag ACK (blokerer indtil EV3-serveren sender “done”)
#         ev3.send(json.dumps({"coords": tasks}))
#         ack = ev3.recv()
#         print("EV3 svarede:", ack)
#         caught_orange = True  # Opdater state, når orange bold er hentet
        
#         while white_balls or caught_orange:
#             # 8) Gentag loopet for næste bold(runde)
#             coords = coord_finder(caught_orange)
#             if not coords or caught_orange and not coords[3]:
#                 print("Ingen koordinater fundet, afslutter.")
#                 break

#             cross      = coords[0]
#             robot_pos  = coords[1]
#             white_balls= coords[3]

#             cross_q   = to_int_cm(cross)
#             robot_q   = to_int_cm(robot_pos)
#             white_qs  = [to_int_cm(pt) for pt in white_balls]

#             tasks = [
#                 {"name": "cross",  "x": cross_q[0],  "y": cross_q[1]},
#                 {"name": "robot",  "x": robot_q[0],  "y": robot_q[1]},
#             ]
#             tasks.append([{"name": "white", "x": x, "y": y} for x, y in white_qs])

#             print("Gitter-koordinater og objekter:", tasks)

#             ev3.send(json.dumps({"coords": tasks}))
#             ack = ev3.recv()
#             print("EV3 svarede:", ack)  
        
#     ev3.close()



def main():
    EV3_IP = "172.20.10.10"
    ev3 = EV3Controller(EV3_IP)
    ev3.s.settimeout(None)
    caught_orange = False
    
    loopCycle = True

    while loopCycle:
        # 1) Find koordinater
        coords = coord_finder(caught_orange)
        if not coords:
            print("Ingen koordinater fundet, afslutter.")
            break

        cross      = coords[0]
        robot_pos  = coords[1]
        if caught_orange:
            white_balls = coords[3]
        else:
            orange_ball= coords[3]
            white_balls= coords[4]

        # 3) Konverter til grid-koordinater
        cross_q  = to_int_cm(cross)
        robot_q  = to_int_cm(robot_pos)
        orange_q = to_int_cm(orange_ball) if orange_ball is not None else None
        white_qs = [to_int_cm(w) for w in white_balls]

        # 4) Byg task-listen
        tasks = [
            {"name": "cross",  "x": cross_q[0],  "y": cross_q[1]},
            {"name": "robot",  "x": robot_q[0],  "y": robot_q[1]},
        ]
        if orange_q is not None:
            tasks.append({"name": "orange", "x": orange_q[0], "y": orange_q[1]})
        
        tasks.append([{"name": "white", "x": x, "y": y} for x, y in white_qs])

        print("Gitter-koordinater og objekter:", tasks)

        # 5) Send coords til EV3 og vent på 'done'
        ev3.send(json.dumps({"coords": tasks}))
        print("Venter på 'done' fra EV3…")
        while True:
            raw = ev3.recv(8192)   
            ack = raw.strip().lower()

            if ack == "done":
                print("EV3 bekræfter 'done'.")
                break
            else:
                print(f"Modtog '{ack}', venter fortsat på 'done'…")

        # 6) Opdater state og eventuel exit
        if orange_ball:
            caught_orange = True
            orange_ball = None
        if not white_balls:
            print("Alle bolde hentet, afslutter.")
            break

    ev3.close()


if __name__ == "__main__":
    main()



# def main():
  
#     # 1) Opsæt EV3-klient
#     EV3_IP = "172.20.10.14"
#     ev3 = EV3Controller(EV3_IP)

#     caught_orange = False  # Husk om den orange bold allerede er hentet

#             # 5) Udtræk koordinater (orange vs. hvide bolde)
#     coords = coord_finder(caught_orange)
#     if not coords:
#         print("Ingen koordinater fundet, afslutter.")
    

#     print("Robot:", coords[1])
#     cross = coords[0]
#     robot = coords[1]
#     orange_ball = coords[3]
#     white_balls = coords[4]

#     cross_q   = to_int_cm(cross)
#     robot_q   = to_int_cm(robot)
#     white_qs  = [to_int_cm(pt) for pt in white_balls]
#     orange_q  = to_int_cm(orange_ball) if orange_ball is not None else None

#     tasks = []
#     tasks.append({"name": "cross", "x": cross_q[0], "y": cross_q[1]})
#     tasks.append({"name": "robot", "x": robot_q[0], "y": robot_q[1]})

#     # orange hvis vi har en
#     if orange_q is not None:
#         tasks.append({"name": "orange", "x": orange_q[0], "y": orange_q[1]})


#     white_list = [
#         {"name": "white", "x": x, "y": y}
#         for x, y in white_qs
#     ]
#     tasks.append(white_list)

#     print("Gitter-koordinater og objekter:", tasks)
#     ev3.send(json.dumps({"coords": tasks}))

#     ack = ev3.recv()
#     print("EV3 svarede:", ack)

#     # 9) Opdater state, når orange bold er hentet
#     if not caught_orange:
#         caught_orange = True

#     # 10) Stop, hvis ingen hvide bolde tilbage
#     if caught_orange and not white_balls:
#         print("Alle hvide bolde samlet ind – færdig.")
#         exit



