# -*- coding: utf-8 -*-
#gridmap.py
from .config import BORDER_MARGIN_CELLS, GRID_WIDTH, GRID_HEIGHT, OBSTACLE_HEIGHT, OBSTACLE_WIDTH

def create_empty_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def add_obstacles(grid, cross_pos,
                  width=OBSTACLE_WIDTH,
                  height=OBSTACLE_HEIGHT):

    x_center, y_center = cross_pos

    half_w = width  // 2
    half_h = height // 2

    x0 = x_center - half_w
    y0 = y_center - half_h

    for y in range(y0, y0 + height):
        for x in range(x0, x0 + width):
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                grid[y][x] = 1
    return grid

def add_border_obstacles(grid, margin_cells=BORDER_MARGIN_CELLS):

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x < margin_cells or x >= GRID_WIDTH  - margin_cells or
                y < margin_cells or y >= GRID_HEIGHT - margin_cells):
                grid[y][x] = 1
    return grid


def print_grid(grid):

    for y in range(len(grid)-1, -1, -1):        # udskriv fra top til bund
        row = grid[y]
        line = ''.join('#' if cell else '.' for cell in row)
        print(line)