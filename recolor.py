from enum import Enum, auto
from PIL import Image
import os 

class Type(Enum):
    GRASS = auto()
    WATER = auto()
    FIRE = auto()


BLACK_BOUND = 0.1
DARK_BOUND = 0.25


def color_amount(elem):
    return elem[0]


def color_ratio(color, pow):
    color_addition = color[1][0]+color[1][1]+color[1][2]
    return (int(color_addition/(255*3)*10**pow)/10**pow)


def is_dark_outline(color):
    color_addition = color[1][0]+color[1][1]+color[1][2]
    return (int(color_addition/(255*3)*100)/100)<0.25


def get_colors_from_image(image):
    colors = image.getcolors()
    colors.sort(key=color_amount, reverse=True)
    return colors


def can_find_black(colors):
    found = 0
    for color in colors :
        ratio = color_ratio(color, 3)
        if ratio < BLACK_BOUND :
            found += 1
            #print("found_black", ratio, color[1])
    return found


"""
def can_find_dark(colors):
    found = 0
    for color in colors :
        ratio = color_ratio(color, 3)
        if BLACK_BOUND < ratio < DARK_BOUND :
            found += 1
            print("found_dark", ratio, color[1])
    return found
"""

def color_analysis(filename):
    im = Image.open("sprites/" + filename)
    colors = get_colors_from_image(im)

    print(filename, colors)
    print(" ")

    im.close()

def main():
    print(" ")
    with os.scandir("sprites") as it:
        for entry in it:
            if entry.name.endswith('.png') and entry.is_file():
                color_analysis(entry.name)


main()