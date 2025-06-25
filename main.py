## main.py
import json
from ImageRecognitionModule.Detecting import coord_finder
from ev3_controller import EV3Controller



def to_int_cm(pt):
    x, y = pt
    return int(round(float(x))), int(round(float(y)))


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


