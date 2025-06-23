# infraredSensor.py

def isBallVeryClose(ir, threshold=15):
    proximity = ir.proximity
    print("[DEBUG] IR proximity", proximity)
    return proximity < threshold
