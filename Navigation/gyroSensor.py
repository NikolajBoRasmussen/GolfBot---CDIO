
import time
from ev3dev2.motor import MoveTank, SpeedPercent

def face_angle(robot, gyro,
                   target_angle,
                   tolerance: float = 0.1,
                   kp: float = 0.8,
                   ki: float = 0.01,
                   kd: float = 0.05,
                   dt: float = 0.01):
    integral = 0.0
    last_error = 0.0
    while True:
        current = gyro.angle
        error   = target_angle - current

        if abs(error) <= tolerance:
            robot.off(brake=True)
            break

        integral += error * dt
        derivative = (error - last_error) / dt
        output = kp*error + ki*integral + kd*derivative

        # begræns motor-output
        speed = max(min(output, 100), -100)
        robot.on(SpeedPercent(speed), SpeedPercent(-speed))

        last_error = error
        time.sleep(dt)



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
