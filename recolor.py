from enum import Enum, auto
from PIL import Image
import os
import math


class Type(Enum):
    GRASS = auto()
    WATER = auto()
    FIRE = auto()


BLACK_COLOR = (16, 16, 16, 255)
HUE_BOUND = 25

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b) 
    cmin = min(r, g, b)   
    diff = cmax-cmin    
    if cmax == cmin:
        h = 0
    elif cmax == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360
    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100
    v = cmax * 100
    return h, s, v


def color_amount(elem):
    return elem[0]


def truncate(value, decimals=3):
    return int(value*(10**decimals))/(10**decimals)


def get_colors_from_image(image):
    colors = image.getcolors()
    colors.sort(key=color_amount, reverse=True)
    return colors


def remove_alpha(colors:list):
    colors.pop(0)
    return colors

def is_gray(color):
    red = color[1][0]
    green = color[1][1]
    blue = color[1][2]
    return red == green == blue

# steel types lmao
def remove_grays(colors:list):
    colors = [color for color in colors if not is_gray(color)]
    return colors

def delta(val_a, val_b):
    delta = abs(val_a-val_b)
    return truncate(delta)


def get_main_color(colors):
    if (colors[0][1] == BLACK_COLOR):
        main_color = colors[1][1]
    else:
        main_color = colors[0][1]
    return main_color


def get_hue(color):
    r, g, b = color[0], color[1], color[2]
    main_hue, _, _ = rgb_to_hsv(r, g, b)
    return truncate(main_hue)


def get_color_cluster(colors):
    color_cluster = []
    main_color = get_main_color(colors)
    main_hue = get_hue(main_color)
    
    for color in colors:
        hue = get_hue(color[1])
        delta_hue = delta(main_hue, hue)
        if delta_hue < HUE_BOUND:
            color_cluster.append(color)
    
    return color_cluster


def show_colors(colors):
    for color in colors:
        print(color)
    print(" ")


def color_analysis(filename):
    im = Image.open("sprites/" + filename)
    
    colors = get_colors_from_image(im)
    colors = remove_alpha(colors)
    colors = remove_grays(colors)

    show_colors(colors)

    main_cluster = get_color_cluster(colors)
    show_colors(main_cluster)

    im.close()


def main():
    print(" ")
    with os.scandir("sprites") as it:
        for entry in it:
            if entry.name.endswith('.png') and entry.is_file():
                color_analysis(entry.name)


main()



"""













(218, (57, 148, 148, 255))
(133, (98, 213, 180, 255))
(88, (115, 172, 49, 255)) 
(67, (24, 74, 74, 255))   
(52, (164, 213, 65, 255)) 
(36, (131, 238, 197, 255))
(35, (82, 98, 41, 255))   
(22, (189, 255, 115, 255))
(14, (189, 41, 32, 255))  
(6, (255, 106, 98, 255))  
(4, (222, 74, 65, 255))   
 
(218, (57, 148, 148, 255))
(133, (98, 213, 180, 255))
(67, (24, 74, 74, 255))   
(36, (131, 238, 197, 255))




















"""