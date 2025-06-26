# # pathfinding.py
# # -*- coding: utf-8 -*-


# """
# Samlet flow i korte træk:
#     Start med kun startnoden i open-list.

#     Gentag: Vælg den mest lovende node (lavest f), flyt den til closed.

#     Hvis det er mål → byg og returner stien.

#     Ellers udforsk dens 4 naboer:

#     Drop dem, der er uden for grid, forhindringer eller allerede i closed.

#     Beregn g, h, lav en ny node, og tilføj til open-list, medmindre vi allerede har en bedre g.

#     Hvis open-list bliver tom → ingen sti.
# """

import heapq
from .config import GRID_WIDTH, GRID_HEIGHT

def heuristic(a, b):
    # Manhattan‐afstand
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    
    open_heap = []
    # G-scores for hver koord
    g_score = { start: 0 }
    # Parent‐pege for path‐rekonstruktion
    came_from = {}
    
    # Hæld start ind i heap med f = h(start)
    heapq.heappush(open_heap, (heuristic(start, goal), start))
    
    while open_heap:
        f, current = heapq.heappop(open_heap)
        if current == goal:
            # Byg path tilbage til start
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            return path[::-1]
        
        x, y = current
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
                continue
            if grid[ny][nx] == 1:
                continue
            
            neighbor = (nx, ny)
            tentative_g = g_score[current] + 1
            
            # Hvis vi fandt en bedre g-score for neighbor:
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_score, neighbor))
    
    # Ingen sti fundet
    return None

