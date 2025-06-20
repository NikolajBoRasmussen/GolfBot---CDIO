#### THIS SENSOR IS ATTACHED TO THE ROBOT ANYMORE

from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_4

us = UltrasonicSensor(INPUT_4) 

def isBallClose(threshold_cm=6):
    """Returnerer True hvis et objekt er tættere end threshold_cm foran sensoren."""
    distance = us.distance_centimeters
    print("distance: ", distance)
    if distance < threshold_cm:
        return True
    elif distance is not None:
        print("NONE")
        return True
    else:
        return False
