# infraredSensor.py

def isBallVeryClose(ir, threshold=7):
    proximity = ir.proximity
    print("[DEBUG] IR proximity", proximity)
    return proximity < threshold
