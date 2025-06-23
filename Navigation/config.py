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
GRID_WIDTH = 168
GRID_HEIGHT = 122

# Robot
ROBOT_WIDTH = 150 ##mm
ROBOT_LENGTH = 250 ##mm
WHEEL_DIAMETER = 55 ##mm
AXLE_TRACK = 120 #90 ##mm
ARM_REACH = 6

# Afstande
STOP_DISTANCE_FROM_BALL = 10
STOP_DISTANCE_FROM_GOAL = 20
DELIVERY_ANGLE_TOLERANCE = 5  # grader
ANGLE_TOLERANCE = 10
POSITIONING_TOLERANCE = 2     # cm

#Positions
ROBOT_START_POS = (10, 10) # GRID (1,1)
#ROBOT_START_POS = ((0 + 10) / GRID_SIZE, ((60) / GRID_SIZE) - INDEX_0)

SAFEPOINT_BIG = (0 + STOP_DISTANCE_FROM_GOAL, GRID_HEIGHT/2)
SAFEPOINT_SMALL = (GRID_WIDTH - STOP_DISTANCE_FROM_GOAL, GRID_HEIGHT/2 )
SAFEPOINTS = [
    SAFEPOINT_BIG,
    SAFEPOINT_SMALL
]


START_POS_CM = (1, 5) ##mm
#START_POS_CM = ((0 + 10) / GRID_SIZE, ((60) / GRID_SIZE) - INDEX_0)  # nu i cm


# Hvor mange celler skal du “inflate” forhindringen med?
OBSTACLE_MARGIN_CELLS = 12

# Hvor bred skal kanten være (i celler)
BORDER_MARGIN_CELLS   = 7
DRIVE_BACK_FROM_BALL = 5
DRIVE_TO_BALL = 12

# Hvor mange celler bred og høj er selve forhindringen?
OBSTACLE_WIDTH  = 20 + 2*OBSTACLE_MARGIN_CELLS 
OBSTACLE_HEIGHT = 20 + 2*OBSTACLE_MARGIN_CELLS 

MIN_SEGMENT_CM = 15 

"""
fra bagenden til midten af hjul: 12cm
fra siderne til midten af hjul: 7cm
fra midten af hjul til forside- arme oppe: 8 cm
fra midten af hjul til forside- arme nede: 14cm
"""







