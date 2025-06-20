# # quantize_coords.py

# import math
# from ImageRecognitionModule. detection_runner import retrieve_coordinates  
# # Antag at dit detektions‐script hedder detection_runner.py 
# # og at retrieve_coordinates() returnerer en liste som:
# # [cross, robot, egg, orange_ball, white_balls]
# # hvor white_balls selv er en liste af [x,y]-par.

# def round_down_to_nearest_10(val: float) -> int:
#     """
#     Runder val ned til nærmeste 10-tal: 
#     fx. 86.7 -> 80, 137.2 -> 130, 9.5 -> 0
#     """
#     return int(math.floor(val / 10) * 10)

# def quantize_coords(coord_list):
#     """
#     Gennemgår hver indgang i coord_list. 
#     Hvis det er et enkelt punkt [x,y], runder vi det. 
#     Hvis det er en liste af punkter (white_balls), kvantiserer vi alle.
#     Returnerer en flad liste af (qx, qy)-tupler.
#     """
#     quantized = []
#     for item in coord_list:
#         # Hvis item er en liste af flere punkter:
#         if isinstance(item, list):
#             for pt in item:
#                 qx = round_down_to_nearest_10(pt[0])
#                 qy = round_down_to_nearest_10(pt[1])
#                 quantized.append((qx, qy))
#         else:
#             # item er et enkelt punkt [x,y]:
#             qx = round_down_to_nearest_10(item[0])
#             qy = round_down_to_nearest_10(item[1])
#             quantized.append((qx, qy))
#     return quantized

# def main():
#     # 1) Hent den rå koordinatliste
#     raw_coords = retrieve_coordinates()
#     if not raw_coords:
#         print("Ingen koordinater fundet.")
#         return

#     # 2) Kvantisér dem alle
#     quantized = quantize_coords(raw_coords)

#     # 3) Print resultatet (eller send det videre til dit navigation-modul)
#     print("Kvantiserede koordinater (ned til nærmeste tier):")
#     print(quantized)

#     # Returnér også, hvis du vil genbruge det i anden kode
#     return quantized

# if __name__ == "__main__":
#     main()
