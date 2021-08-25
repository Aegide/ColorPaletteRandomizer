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


def remove_alpha(colors:list):
    colors.pop(0)
    for color in colors:
        print(color)
    print(" ")


def color_analysis(filename):
    im = Image.open("sprites/" + filename)
    colors = get_colors_from_image(im)
    colors = remove_alpha(colors)
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
(118, (16, 16, 16, 255))  
(88, (115, 172, 49, 255)) 
(67, (24, 74, 74, 255))   
(52, (164, 213, 65, 255)) 
(36, (131, 238, 197, 255))
(35, (82, 98, 41, 255))   
(22, (189, 255, 115, 255))
(21, (255, 255, 255, 255))
(14, (189, 41, 32, 255))  
(10, (205, 205, 205, 255))
(6, (255, 106, 98, 255))  
(4, (222, 74, 65, 255)) 


"""