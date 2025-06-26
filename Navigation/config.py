# -*- coding: utf-8 -*-
#config.py 

"""
Robotten starter i grid (1,1), mos øst (0 grader)
Det store mål er hele punkt (0,5) og (0,6)
det lille mål er indtil videre hele punkt (17,5) og (17,6).  Overvej at gøre grids mindre.
"""
INDEX_0 = 1

# Grid
GRID_SIZE = 1  # cm
# Bane

FIELD_WIDTH = 168
FIELD_HEIGHT = 122

GRID_WIDTH = FIELD_WIDTH // GRID_SIZE
GRID_HEIGHT = FIELD_HEIGHT // GRID_SIZE

# Robot
ROBOT_WIDTH = 150 ##mm
ROBOT_LENGTH = 250 ##mm
WHEEL_DIAMETER = 55 ##mm
AXLE_TRACK = 120 #90 ##mm
ARM_REACH = 6

# Afstande
STOP_DISTANCE_FROM_BALL = 8
STOP_DISTANCE_FROM_GOAL = 20
DELIVERY_ANGLE_TOLERANCE = 5  # grader
ANGLE_TOLERANCE = 10
POSITIONING_TOLERANCE = 2     # cm

#Positions
ROBOT_START_POS = (10, 10) 

SAFEPOINT_BIG = (0 + STOP_DISTANCE_FROM_GOAL, GRID_HEIGHT/2)
SAFEPOINT_SMALL = (GRID_WIDTH - STOP_DISTANCE_FROM_GOAL, GRID_HEIGHT/2 )
SAFEPOINTS = [
    SAFEPOINT_BIG,
    SAFEPOINT_SMALL
]

SAFEZONE_X = 25
SAFEZONE_Y = 25
SAFEZONE1 = (SAFEZONE_X, SAFEZONE_Y)
SAFEZONE2 = (GRID_WIDTH-SAFEZONE_X, SAFEZONE_Y)
SAFEZONE3 = (GRID_WIDTH-SAFEZONE_X, GRID_HEIGHT-SAFEZONE_Y)
SAFEZONE4 = (SAFEZONE_X, GRID_HEIGHT-SAFEZONE_Y)
SAFEZONES = [SAFEZONE1, SAFEZONE2, SAFEZONE3, SAFEZONE4]

START_POS_CM = (1, 5) ##mm

QUADRANT_1 = ((84.0, 61.0), (168.0, 122.0))  # Øverste højre
QUADRANT_2 = ((0.0,  61.0), (84.0,  122.0))  # Øverste venstre
QUADRANT_3 = ((0.0,   0.0), (84.0,   61.0))  # Nederste venstre
QUADRANT_4 = ((84.0,  0.0), (168.0,  61.0))  # Nederste højre


MID_REGION_X_MIN = 56
MID_REGION_X_MAX = 112
MID_REGION_Y_MIN = 39
MID_REGION_Y_MAX = 83


OBSTACLE_MARGIN_CELLS = 14

# Hvor bred skal kanten være (i celler)
BORDER_MARGIN_CELLS   = 10
DRIVE_BACK_FROM_BALL = 5
DRIVE_TO_BALL = 12

OBSTACLE_WIDTH  = 20 + 2*OBSTACLE_MARGIN_CELLS 
OBSTACLE_HEIGHT = 20 + 2*OBSTACLE_MARGIN_CELLS 




"""
fra bagenden til midten af hjul: 12cm
fra siderne til midten af hjul: 7cm
fra midten af hjul til forside- arme oppe: 8 cm
fra midten af hjul til forside- arme nede: 14cm
"""







