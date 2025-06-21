
import time
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor       import MoveTank, SpeedPercent

def face_angle(robot, gyro,
               target_angle: float,
               tolerance: float = 1.0,
               kp: float = 0.8):
    while True:
        current = gyro.angle
        error   = target_angle - current
        if abs(error) <= tolerance:
            robot.off(brake=True)
            break
        
        speed = kp * error
        speed = max(min(speed, 100), -100)
        robot.on(SpeedPercent(speed), SpeedPercent(-speed))
        time.sleep(0.01)


def face_opposite(robot, gyro,
                  tolerance: float = 1.0,
                  kp: float = 0.8):
    face_angle(robot, gyro, 180.0, tolerance, kp)



def turn_and_report(robot: MoveTank, gyro,
                    angle: float,
                    tolerance: float = 1.0,
                    kp: float = 0.8):

    start = gyro.angle
    face_angle(robot, angle, tolerance, kp)
    end = gyro.angle
    actual = end - start
    print("⚙️  Målt rotation: {:.1f}° (mål: {:.1f}°) – Total gyro‐vinkel nu: {:.1f}°"
          .format(actual, angle, end))
