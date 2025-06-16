import socket
import time
# Henter ensorer, motorer etc. fra ev3dev2 biblioteket
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank

#####################################################################
##                                                                 ##
##                 NEDENSTÅENDE ER DUMMY-KODE                      ##
##    DER SKAL ÆNDRINGER FOR AT TILPASSE JERES ANDRES PROGRAMMER   ##
##                                                                 ##
#####################################################################


# Initialiserer hardware
# GyroSensor til at tracke rotation
gyro = GyroSensor()
# Motorer til at køre robotten
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

# Kalibrerer gyro sensor ved at nulstille den
def reset_gyro():
    print("Calibrating gyro sensor...")
    gyro.reset()
    # Giver tid til at gyroen stabiliserer sig
    #OBS - Kameeraet HADER time.sleep() funktionen, da den fryser hele programmet.
    #Derfor råder jeg til at overveje hvornår gyrosensoren skal kalibreres, og om det er nødvendigt at gøre det hver gang.
    # time.sleep(2)  Normalt set ville jeg bruge denne, men da kameraet fryser, så det er ikke en god idé at undgå den så vidt muligt.
    print("Gyro calibration done.")

#Definerer kommandoerne til robotten - Flere kan tilføjes/ændres om nødvendigt.
#Hvis i vil kalde det noget andet end robot_commands, så skal i ændre det i start_server funktionen (på linje 69 eller deromkring)
#Evt. gør ligesom med gyro_calibrate funktionen og definer jeres funktioner separat.over de forskellige kommandoer, og så indsæt dem herunder med de ønskede kommando navne.
#Husk man altid kan tilføje flere argumenter og bruge dem i kommandoerne, hvis det er nødvendigt.
def robot_commands(command, angle, speed, distance):
    if command == "forward":
        tank_drive.on_for_seconds(SpeedPercent(60), SpeedPercent(30), 3)
    elif command == "left":
        tank_drive.on_for_seconds(SpeedPercent(-20), SpeedPercent(20),2)
    elif command == "right":
        tank_drive.on_for_seconds(SpeedPercent(20), SpeedPercent(-20),2)
    elif command == "stop":
        tank_drive.off()
    elif command == "gyro_calibrate":
        reset_gyro()
    else:
        print("Unknown command: {}".format(command))

# Serveren lytter på kommandoer fra klienter (i dette tilfælde vores computere) og styrer robotten baseret på modtagne kommandoer
# Koden herfra og ned er simpel, men vigtig for at kunne modatge de forskellige kommandoer.
def start_server():
    HOST = ''
    PORT = 9999
    # Opretter en socket for at lytte på kommandoer
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print("Server lytter på port {}...".format(PORT))

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
                    robot_commands(message)


if __name__ == "__main__":
    start_server()
