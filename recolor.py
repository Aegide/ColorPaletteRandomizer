from enum import Enum, auto
from PIL import Image
import os
import math


class Type(Enum):
    GRASS = auto()
    WATER = auto()
    FIRE = auto()


BLACK_COLOR = (16, 16, 16, 255)
COLOR_DELTA_BOUND = 125


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


def truncate(value, decimals):
    return int(value*(10**decimals))/(10**decimals)



def get_colors_from_image(image):
    colors = image.getcolors()
    colors.sort(key=color_amount, reverse=True)
    return colors


def remove_alpha(colors:list):
    colors.pop(0)


def color_delta(color_a, color_b):
    red = color_a[0] - color_b[0]
    green = color_a[1] - color_b[1]
    blue = color_a[2] - color_b[2]
    delta = math.sqrt(red**2 + green**2 + blue**2)
    return delta 


def color_clusters(colors):
    if (colors[0][1] == BLACK_COLOR):
        main_color = colors.pop(1)[1]
    else:
        main_color = colors.pop(0)[1]
    print(main_color)
    for color in colors:
        delta = color_delta(main_color, color[1])
        delta = truncate(delta, 2)
        print(color[1], delta)
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
(98, 213, 180, 255) 83.24
(16, 16, 16, 255) 191.12
(115, 172, 49, 255) 117.22
(24, 74, 74, 255) 109.73
(164, 213, 65, 255) 150.2
(131, 238, 197, 255) 126.4
(82, 98, 41, 255) 120.72
(189, 255, 115, 255) 173.09
(255, 255, 255, 255) 249.2
(189, 41, 32, 255) 205.74
(205, 205, 205, 255) 168.52
(255, 106, 98, 255) 208.48
(222, 74, 65, 255) 198.97












"""