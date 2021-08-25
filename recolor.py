from enum import Enum, auto
from PIL import Image
import os
import math


class Type(Enum):
    GRASS = auto()
    WATER = auto()
    FIRE = auto()


BLACK_COLOR = (16, 16, 16, 255)


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


def delta(val_a, val_b):
    delta = math.sqrt(val_a**2 + val_b**2)
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


def color_clusters(colors):
    main_color = get_main_color(colors)
    main_hue = get_hue(main_color)
    
    print(main_color, "\n")
    for color in colors:
        hue = get_hue(color[1])
        delta_hue = delta(main_hue, hue)
        print(color[1], hue, delta_hue)
    print(" ")


def show_colors(colors):
    for color in colors:
        print(color)
    print(" ")


def color_analysis(filename):
    im = Image.open("sprites/" + filename)
    colors = get_colors_from_image(im)
    # show_colors(colors)
    remove_alpha(colors)
    color_clusters(colors)
    im.close()


def main():
    print(" ")
    with os.scandir("sprites") as it:
        for entry in it:
            if entry.name.endswith('.png') and entry.is_file():
                color_analysis(entry.name)


main()



"""
















(57, 148, 148, 255) 


(24, 74, 74, 255)       180.0       254.558
(57, 148, 148, 255)     180.0       254.558  
(98, 213, 180, 255)     162.782     242.689
(131, 238, 197, 255)    157.009     238.855


(82, 98, 41, 255)       76.842      195.715
(115, 172, 49, 255)     87.804      200.273
(164, 213, 65, 255)     79.864      196.921
(189, 255, 115, 255)    88.285      200.485


(189, 41, 32, 255)      3.439       180.032
(255, 106, 98, 255)     3.057       180.025
(222, 74, 65, 255)      3.439       180.032


(16, 16, 16, 255)       0.0         180.0
(205, 205, 205, 255)    0.0         180.0
(255, 255, 255, 255)    0.0         180.0







"""