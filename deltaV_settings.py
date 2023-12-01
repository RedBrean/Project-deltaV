WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

file_name = "solar_system.txt"

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D

def color_from_str(string:str):
    if(string.lower() == "red"):
        return RED