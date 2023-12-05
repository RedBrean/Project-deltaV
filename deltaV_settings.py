WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

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
    elif(string.lower() == "blue"):
        return BLUE
    elif(string.lower() == "yellow"):
        return YELLOW
    elif(string.lower() == "green"):
        return GREEN
    elif(string.lower() == "magenta"):
        return MAGENTA
    elif(string.lower() == "cyan"):
        return CYAN
    elif(string.lower() == "black"):
        return BLACK
    elif(string.lower() == "white"):
        return WHITE
    elif(string.lower() == "grey"):
        return GREY
    else:
        print("no color recognised")
        return WHITE
    
    