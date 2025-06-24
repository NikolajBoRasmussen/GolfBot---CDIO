# infraredSensor.py

def isBallVeryClose(ir, threshold=13):
    proximity = ir.proximity
    print("[DEBUG] IR proximity", proximity)
    return proximity < threshold
