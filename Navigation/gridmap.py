# -*- coding: utf-8 -*-

from .config import GRID_WIDTH, GRID_HEIGHT

 
# Returnerer en tom grid som en liste af lister,
# hvor hver celle er 0 (fri).
# Dimension: GRID_HEIGHT rækker x GRID_WIDTH kolonner.
# Grid = 18 x 12 felter
def create_empty_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


# Indsætter en 2x2 forhindring (værdien 1) midt i grid’et.
# Vi udnytter, at midten er ved indekser GRID_WIDTH//2 og GRID_HEIGHT//2.
def add_obstacles(grid):
   
    mid_x = GRID_WIDTH // 2
    mid_y = GRID_HEIGHT // 2

    # Forhindringen fylder to celler på hver side af midten:
    for y in range(mid_y - 1, mid_y + 1):
        for x in range(mid_x - 1, mid_x + 1):
            grid[y][x] = 1  # 1 betyder forhindring
    return grid #returnere nyt grid med de celler der er optaget


def inflate_obstacles(grid, margin=1):
    new_grid = [row[:] for row in grid]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                for dy in range(-margin, margin+1):
                    for dx in range(-margin, margin+1):
                        ny, nx = y + dy, x + dx
                        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                            new_grid[ny][nx] = 1
    return new_grid


def add_border_obstacles(grid, margin_cells=1):
    """
    Marker alle celler inden for `margin_cells` fra kanten som forhindringer.
    margin_cells=1 vil blokere første række/kolonne og sidste.
    """
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if x < margin_cells or x >= GRID_WIDTH - margin_cells \
            or y < margin_cells or y >= GRID_HEIGHT - margin_cells:
                grid[y][x] = 1
    return grid
