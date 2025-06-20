# -*- coding: utf-8 -*-

"""
Robotten starter i grid (1,1), mos øst (0 grader)
Det store mål er hele punkt (0,5) og (0,6)
det lille mål er indtil videre hele punkt (17,5) og (17,6).  Overvej at gøre grids mindre.
"""
INDEX_0 = 1

# Grid
GRID_SIZE = 10  # cm
GRID_WIDTH = 17  # 180 cm / 10 cm
GRID_HEIGHT = 12 

# Bane
FIELD_WIDTH = 170  # cm 
FIELD_HEIGHT = 120  # cm

# Robot
ROBOT_WIDTH = 150 ##mm
ROBOT_LENGTH = 250 ##mm
WHEEL_DIAMETER = 55 ##mm
AXLE_TRACK = 120 #90 ##mm
ARM_REACH = 6

# Afstande
STOP_DISTANCE_FROM_BALL = 3
STOP_DISTANCE_FROM_GOAL = 10
DELIVERY_ANGLE_TOLERANCE = 5  # grader
POSITIONING_TOLERANCE = 2     # cm

#Positions
#ROBOT_START_POS = (10//GRID_SIZE, 10//GRID_SIZE) # GRID (1,1)
ROBOT_START_POS = (10, 10) # GRID (1,1)
#ROBOT_START_POS = ((0 + 10) / GRID_SIZE, ((60) / GRID_SIZE) - INDEX_0)
SAFEPOINT_BIG = (10/GRID_SIZE, ((FIELD_HEIGHT/2)/GRID_SIZE)-INDEX_0)
SAFEPOINT_SMALL = (150/GRID_SIZE, ((FIELD_HEIGHT/2)/GRID_SIZE)-INDEX_0)
SAFEPOINTS = [
    SAFEPOINT_BIG,
    SAFEPOINT_SMALL
]


START_POS_CM = (1, 5) ##mm
#START_POS_CM = ((0 + 10) / GRID_SIZE, ((60) / GRID_SIZE) - INDEX_0)  # nu i cm

"""
fra bagenden til midten af hjul: 12cm
fra siderne til midten af hjul: 7cm
fra midten af hjul til forside- arme oppe: 8 cm
fra midten af hjul til forside- arme nede: 14cm
"""







