#!/usr/bin/env pybricks-micropython

# This program is a simple example of how to use the EV3 Brick and Motor classes from the Pybricks library.
# It initializes an EV3 Brick and a motor, plays a sound, runs the motor to a target angle, and plays another sound.
#from pybricks import EV3brick as brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
#from pybricks import ev3brick as brick
#from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
#                                 InfraredSensor, UltrasonicSensor, GyroSensor)
#from pybricks.parameters import (Port, Stop, Direction, Button, Color,
#                                 SoundFile, ImageFile, Align)
#from pybricks.tools import print, wait, StopWatch
#from pybricks.robotics import DriveBase

# Create your objects here

def main ():
# Initialize the EV3 Brick.
    ev3 = EV3Brick()

# Initialize a motor at port B.
    test_motor = Motor(Port.B)

# Write your program here

# Play a sound.
    ev3.speaker.beep()

# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
    test_motor.run_target(500, 90)

# Play another beep sound.
    ev3.speaker.beep(frequency=1000, duration=500)
