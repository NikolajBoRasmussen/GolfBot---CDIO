# -*- coding: utf-8 -*-

from .config import BORDER_MARGIN_CELLS, GRID_WIDTH, GRID_HEIGHT, OBSTACLE_HEIGHT, OBSTACLE_MARGIN_CELLS, OBSTACLE_WIDTH

def create_empty_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def add_obstacles(grid,
                  width=OBSTACLE_WIDTH,
                  height=OBSTACLE_HEIGHT):

    mid_x = GRID_WIDTH  // 2
    mid_y = GRID_HEIGHT // 2

    half_w = width  // 2
    half_h = height // 2

    x0 = mid_x - half_w
    y0 = mid_y - half_h

    for y in range(y0, y0 + height):
        for x in range(x0, x0 + width):
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                grid[y][x] = 1
    return grid

def inflate_obstacles(grid, margin=OBSTACLE_MARGIN_CELLS):

    new_grid = [row[:] for row in grid]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                for dy in range(-margin, margin+1):
                    for dx in range(-margin, margin+1):
                        ny, nx = y + dy, x + dx
                        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                            new_grid[ny][nx] = 1

    print("Tjek celle (85,60):", grid[60][85])  # skal printe 1
    print("Tjek celle (99,46):", grid[46][99])  # skal printe 1

    return new_grid

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