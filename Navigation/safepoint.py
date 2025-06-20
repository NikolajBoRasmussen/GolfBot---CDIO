# safepoint.py

import math

from .config import SAFEPOINTS

# Liste over dine to safepoints i (col, row)-format


def nearest_safepoint(ball_cell, safepoints=SAFEPOINTS):
    """
    Returnerer den (col, row) fra safepoints-listen,
    der er tættest på ball_cell.
    """
    distances = []
    for sp in safepoints:
        dx = sp[0] - ball_cell[0]
        dy = sp[1] - ball_cell[1]
        distances.append((math.hypot(dx, dy), sp))
    _, nearest = min(distances, key=lambda t: t[0])
    return (int(nearest[0]), int(nearest[1]))