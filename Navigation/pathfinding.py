# pathfinding.py
# -*- coding: utf-8 -*-


"""
Samlet flow i korte træk:
    Start med kun startnoden i open-list.

    Gentag: Vælg den mest lovende node (lavest f), flyt den til closed.

    Hvis det er mål → byg og returner stien.

    Ellers udforsk dens 4 naboer:

    Drop dem, der er uden for grid, forhindringer eller allerede i closed.

    Beregn g, h, lav en ny node, og tilføj til open-list, medmindre vi allerede har en bedre g.

    Hvis open-list bliver tom → ingen sti.
"""

import math
from .config import GRID_WIDTH, GRID_HEIGHT

"""
Forklaring:

__init__:

    x, y: Gitter-placeringen af noden.

    g: Den kendte afstand (antal trin) fra start til denne node. Ved start er g=0.

    h: Heuristikken – et optimistisk skøn over, hvor mange trin der er tilbage til målet.

    parent: Peger til den node, vi kom fra. Bruges til senere at rekonstruere den fulde sti.

f:

    En “property”, så man kan skrive node.f i stedet for node.g + node.h.

    A* vælger altid den node med lavest f i open-list.
"""
class Node:
    def __init__(self, x, y, g=0, h=0, parent=None):
        self.x, self.y = x, y
        self.g = g
        self.h = h
        self.parent = parent

    @property
    def f(self):
        return self.g + self.h

"""
Beregner Manhattan-afstand mellem to noder a og b.

Returnerer antallet af “gitter-skridt” lodret + vandret, hvis man ignorerer forhindringer.

Bruges som h i hver ny node.
"""
def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

"""
properties i funktionen:
    grid: 2D-liste med 0 = fri og 1 = forhindring.
    start/goal: Tuple (x, y) for start- og mål-celler.

intialisering:
    start_node: Opretter en Node for start med g=0 og h= afstand til mål.
    open_list: Liste af noder, vi skal udforske. Starter kun med startnoden.
    closed: Sæt af koordinater, som vi allerede har undersøgt; bruges til at undgå revisits.
"""
def astar(grid, start, goal):
    open_list = [Node(*start, g=0, h=heuristic(Node(*start), Node(*goal)))]
    closed = set()

    while open_list: #Kør så længe der stadig er noder at undersøge.

        current = min(open_list, key=lambda o: o.f) #Finder den node i open_list med lavest f = g + h. Den er mest “lovende”.

        """
        Hvis den valgte node er mål-cellen, genopbygger vi stien:
        Start fra current, følg parent-pegerne tilbage til start.
        Gem alle (x,y)-koordinater undervejs.
        Brug [::-1] til at vende listen, så den går fra start → mål.
        """
        if (current.x, current.y) == goal:
            path = []

            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        # Fjerner current fra open_list, så vi ikke ser på den igen.
        # Tilføjer dens koordinater til closed, så vi ignorerer den i fremtiden.
        open_list.remove(current)
        closed.add((current.x, current.y))

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]: #Løber gennem de fire mulige retninger (øst, vest, syd, nord).
            nx, ny = current.x+dx, current.y+dy

            # Uden for grid? Spring over.
# Forhindring eller allerede besøgt? Spring over.
            if not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
                continue
            if grid[ny][nx] == 1 or (nx, ny) in closed:
                continue

            """
            g_new: Én skridt mere end vi havde til current.
            h_new: Manhattan-estimat fra nabo til mål.
            neighbor: Ny node med alle værdier + parent=current.
            """
            g_new = current.g + 1
            h_new = heuristic(Node(nx, ny), Node(*goal))
            neighbor = Node(nx, ny, g=g_new, h=h_new, parent=current)

            # Søger i open_list efter en eksisterende node med samme koordinat.
            # Hvis den eksisterende har lavere eller lig g-værdi, er vores nye sti ikke bedre → drop.
            
            existing = next((o for o in open_list if (o.x,o.y)==(nx,ny)), None)
            if existing and neighbor.g >= existing.g:
                continue
            open_list.append(neighbor) #Hvis vi ikke droppede, tilføjer vi neighbor til open_list for fremtidig udforskning.

    return None