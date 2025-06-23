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

# import math
# from .config import GRID_WIDTH, GRID_HEIGHT

# class Node:
#     def __init__(self, x, y, g=0, h=0, parent=None):
#         self.x, self.y = x, y
#         self.g = g
#         self.h = h
#         self.parent = parent

#     @property
#     def f(self):
#         return self.g + self.h

# def heuristic(a, b):
#     return abs(a.x - b.x) + abs(a.y - b.y)


# def astar(grid, start, goal):
#     open_list = [Node(*start, g=0, h=heuristic(Node(*start), Node(*goal)))]
#     closed = set()

#     while open_list: #Kør så længe der stadig er noder at undersøge.

#         current = min(open_list, key=lambda o: o.f) #Finder den node i open_list med lavest f = g + h. Den er mest “lovende”.

#         if (current.x, current.y) == goal:
#             path = []

#             while current:
#                 path.append((current.x, current.y))
#                 current = current.parent
#             return path[::-1]

#         open_list.remove(current)
#         closed.add((current.x, current.y))

#         for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]: #Løber gennem de fire mulige retninger (øst, vest, syd, nord).
#             nx, ny = current.x+dx, current.y+dy

#             if not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
#                 continue
#             if grid[ny][nx] == 1 or (nx, ny) in closed:
#                 continue

#             g_new = current.g + 1
#             h_new = heuristic(Node(nx, ny), Node(*goal))
#             neighbor = Node(nx, ny, g=g_new, h=h_new, parent=current)

#             # Søger i open_list efter en eksisterende node med samme koordinat.
#             # Hvis den eksisterende har lavere eller lig g-værdi, er vores nye sti ikke bedre → drop.
            
#             existing = next((o for o in open_list if (o.x,o.y)==(nx,ny)), None)
#             if existing and neighbor.g >= existing.g:
#                 continue
#             open_list.append(neighbor) #Hvis vi ikke droppede, tilføjer vi neighbor til open_list for fremtidig udforskning.

#     return None

# pathfinding.py
# -*- coding: utf-8 -*-

import heapq
from .config import GRID_WIDTH, GRID_HEIGHT, STOP_DISTANCE_FROM_BALL

def heuristic(a, b):
    # Manhattan‐afstand
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    
    # print("GRID I ASTAR")
    # for y in range(len(grid)-1, -1, -1):        # udskriv fra top til bund
    #     row = grid[y]
    #     line = ''.join('#' if cell else '.' for cell in row)
    #     print(line)

    # Min‐heap: hvert entry er (f_score, x, y)
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

