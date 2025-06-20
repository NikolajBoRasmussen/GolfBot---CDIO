# -*- coding: utf-8 -*-

"""
ascii_route_printer.py
Hjælpefunktioner til at udskrive ruter på en ASCII-grid.
Designet til at kunne kopieres direkte ind i EV3 MicroPython, uden eksterne afhængigheder eller f-strings.
"""

def print_ascii_route(grid, full_path, start, safepoint, goal, segments=None):
    """
    Print et ASCII-kort af occupancy grid med forskellige symboler:
    - '#': forhindring
    - '.': fri celle
    - 'B': startposition (base)
    - 'S': safepoint
    - 'E': slutposition
    - '+': rute fra start til bold
    - '*': rute fra bold til safepoint
    - '-': rute fra safepoint til start

    Hver print() kalder kun én streng, så EV3 MicroPython kan håndtere det.
    """
    # Konverter segmenter til sæt for lookup
    if segments:
        seg0 = set(segments[0])
        seg1 = set(segments[1])
        seg2 = set(segments[2])
    else:
        seg0 = seg1 = seg2 = set()
    full_set = set(full_path)

    # Legend
    legend = ("#=obstacle", ".=free", "B=start", "S=safepoint",
              "E=end", "+=start->ball", "*=ball->safepoint", "-=safepoint->start")
    print("Legend: " + ",".join(legend))

    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        line = ""
        for x in range(width):
            coord = (x, y)
            # Marker specialpunkter
            if coord == start:
                ch = 'B'
            elif coord == safepoint:
                ch = 'S'
            elif coord == goal:
                ch = 'E'
            # Marker segmenter
            elif coord in seg0:
                ch = '+'
            elif coord in seg1:
                ch = '*'
            elif coord in seg2:
                ch = '-'
            # Forhindringer vs fri
            elif grid[y][x] != 0:
                ch = '#'
            else:
                ch = '.'
            line = line + ch
        print(line)


def print_full_route(grid, segments):
    """
    Samler segmenterne og printer hele ruten.
    """
    # Saml uden at duplikere krydsningspunkter
    full = []
    for seg in segments:
        if full and seg and full[-1] == seg[0]:
            for p in seg[1:]:
                full.append(p)
        else:
            for p in seg:
                full.append(p)

    base = segments[0][0]
    safe = segments[1][0]
    endp = segments[2][-1]

    # Print overskrift uden f-strings
    head = "Hele ruten fra B=" + str(base) + " til E=" + str(endp) + " via S=" + str(safe)
    print(head)
    print_ascii_route(grid, full, base, safe, endp, segments)
