# perception.py

import math
from typing import Tuple, List
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, START_POS_CM

# Type-aliaser for klarhed
CoordCM = Tuple[float, float]    # (x, y) i centimeter
CoordGrid = Tuple[int, int]      # (col, row) i grid-indeks

def closest_ball(robot: CoordCM, balls: List[CoordCM]) -> Tuple[int, CoordCM, float]:
    """
    Finder den nærmeste bold til robotten.

    Args:
        robot: (x, y) i cm for robot.
        balls: Liste af (x, y) i cm for hver bold.

    Returns:
        idx:   Indeks i balls-listen på den nærmeste bold.
        coord: Koordinater (x, y) for den nærmeste bold.
        dist:  Euklidisk afstand i cm.
    """
    xr, yr = robot
    distances = [
        (math.hypot(x - xr, y - yr), i, (x, y))
        for i, (x, y) in enumerate(balls)
    ]
    dist, idx, coord = min(distances, key=lambda t: t[0])
    return idx, coord, dist

