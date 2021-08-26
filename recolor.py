from enum import Enum, auto
from PIL import Image
import os
import math


BLACK_COLOR = (16, 16, 16, 255)


# 42.3 max
HUE_BOUND = 42

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


def is_gray(color):
    red = color[1][0]
    green = color[1][1]
    blue = color[1][2]
    return red == green == blue


# steel types lmao
def remove_grays(colors:list):
    for color in list(colors):
        if is_gray(color):
            colors.remove(color)


def hue_delta(hua_a, hue_b):
    delta = abs(hua_a - hue_b)
    if ( delta > 180 ):
        delta = 360 - delta
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


# TODO : upgrade this
def get_color_cluster(colors:list):
    color_cluster = []
    cluster_size = 0
    main_color = get_main_color(colors)
    main_hue = get_hue(main_color)
    for color in list(colors):
        hue = get_hue(color[1])
        delta_hue = hue_delta(main_hue, hue)
        if delta_hue < HUE_BOUND:
            color_cluster.append(color)
            cluster_size += 1
            colors.remove(color)
    return color_cluster, cluster_size


def show_colors(colors):
    for color in colors:
        print(color)
    print(" ")


def get_clusters(colors:list):
    clusters = []
    amount_colours = len(colors)
    while(amount_colours > 0):
        color_cluster, cluster_size = get_color_cluster(colors)
        amount_colours = amount_colours - cluster_size
        clusters.append(color_cluster)
        show_colors(color_cluster)
    return clusters


def show_clusters(clusters:list):
    for cluster in clusters:
        print(cluster)
    print("\n\n")


def color_analysis(filename):
    im = Image.open("sprites/" + filename)
    colors = get_colors_from_image(im)
    # show_colors(colors)
    remove_alpha(colors)
    remove_grays(colors)
    clusters = get_clusters(colors)
    im.close()
    return clusters


def main():
    print(" ")
    with os.scandir("sprites") as it:
        for entry in it:
            if entry.name.endswith('.png') and entry.is_file():
                print(entry.name)
                clusters = color_analysis(entry.name)
                print(len(clusters))
                show_clusters(clusters)



main()


"""

























2.png
(368, (49, 123, 164, 255))
(155, (98, 180, 205, 255))
(113, (16, 65, 74, 255))
(29, (139, 213, 246, 255))
 
(171, (74, 139, 32, 255))
(114, (16, 82, 32, 255))
(91, (106, 180, 32, 255))
(14, (131, 230, 90, 255))
 
(99, (213, 65, 90, 255))
(59, (255, 123, 123, 255))
(24, (123, 49, 41, 255))
(21, (255, 172, 164, 255))
 
3
[(368, (49, 123, 164, 255)), (155, (98, 180, 205, 255)), (113, (16, 65, 74, 255)), (29, (139, 213, 246, 255))]
[(171, (74, 139, 32, 255)), (114, (16, 82, 32, 255)), (91, (106, 180, 32, 255)), (14, (131, 230, 90, 255))]   
[(99, (213, 65, 90, 255)), (59, (255, 123, 123, 255)), (24, (123, 49, 41, 255)), (21, (255, 172, 164, 255))]  



4.png
(212, (255, 148, 65, 255))
(191, (222, 82, 57, 255))
(108, (139, 41, 0, 255))
(53, (255, 213, 123, 255))
(44, (230, 172, 90, 255))
(38, (230, 57, 0, 255))
(18, (255, 213, 8, 255))
(13, (246, 164, 0, 255))
(12, (255, 197, 98, 255))

(7, (24, 74, 49, 255))
(3, (65, 164, 123, 255))

(1, (148, 205, 222, 255))

3
[(212, (255, 148, 65, 255)), (191, (222, 82, 57, 255)), (108, (139, 41, 0, 255)), (53, (255, 213, 123, 255)), (44, (230, 172, 90, 255)), (38, (230, 57, 0, 255)), (18, (255, 213, 8, 255)), (13, (246, 164, 0, 255)), (12, (255, 197, 98, 255))]
[(7, (24, 74, 49, 255)), (3, (65, 164, 123, 255))]
[(1, (148, 205, 222, 255))]



5.png
(407, (213, 41, 82, 255))
(226, (255, 82, 74, 255))
(116, (148, 32, 16, 255))
(83, (255, 65, 0, 255))
(6, (255, 148, 123, 255))

(67, (255, 213, 106, 255))
(62, (230, 172, 90, 255))
(43, (255, 222, 41, 255))
(23, (255, 164, 0, 255))

2
[(407, (213, 41, 82, 255)), (226, (255, 82, 74, 255)), (116, (148, 32, 16, 255)), (83, (255, 65, 0, 255)), (6, (255, 148, 123, 255))]
[(67, (255, 213, 106, 255)), (62, (230, 172, 90, 255)), (43, (255, 222, 41, 255)), (23, (255, 164, 0, 255))]



6.png
(795, (238, 131, 41, 255))
(752, (205, 82, 65, 255))
(310, (238, 222, 123, 255))
(308, (238, 180, 90, 255))
(234, (131, 49, 24, 255))
(89, (230, 65, 16, 255))
(54, (255, 213, 16, 255))
(26, (246, 164, 16, 255))

(325, (8, 65, 82, 255))
(288, (32, 115, 148, 255))

2
[(795, (238, 131, 41, 255)), (752, (205, 82, 65, 255)), (310, (238, 222, 123, 255)), (308, (238, 180, 90, 255)), (234, (131, 49, 24, 255)), (89, (230, 65, 16, 255)), (54, (255, 213, 16, 255)), (26, (246, 164, 16, 255))]
[(325, (8, 65, 82, 255)), (288, (32, 115, 148, 255))]



7.png
(231, (90, 172, 156, 255))
(140, (148, 213, 205, 255))
(93, (65, 115, 98, 255))
(15, (180, 246, 238, 255))

(53, (230, 172, 90, 255))
(36, (205, 123, 41, 255))
(34, (123, 49, 8, 255))
(31, (255, 213, 106, 255))
(23, (205, 197, 197, 255))
(19, (98, 41, 0, 255))
(19, (189, 106, 0, 255))
(5, (213, 148, 82, 255))

2
[(231, (90, 172, 156, 255)), (140, (148, 213, 205, 255)), (93, (65, 115, 98, 255)), (15, (180, 246, 238, 255))]
[(53, (230, 172, 90, 255)), (36, (205, 123, 41, 255)), (34, (123, 49, 8, 255)), (31, (255, 213, 106, 255)), (23, (205, 197, 197, 255)), (19, (98, 41, 0, 255)), (19, (189, 106, 0, 255)), (5, (213, 148, 82, 255))]



8.png
(291, (98, 106, 197, 255))
(287, (148, 139, 238, 255))
(271, (180, 205, 222, 255))
(168, (65, 65, 123, 255))
(55, (222, 230, 238, 255))
(21, (197, 189, 255, 255))

(180, (197, 148, 65, 255))
(109, (222, 197, 139, 255))
(45, (139, 90, 32, 255))
(30, (90, 57, 8, 255))
(16, (148, 98, 98, 255))
(1, (205, 131, 32, 255))

2
[(291, (98, 106, 197, 255)), (287, (148, 139, 238, 255)), (271, (180, 205, 222, 255)), (168, (65, 65, 123, 255)), (55, (222, 230, 238, 255)), (21, (197, 189, 255, 255))]
[(180, (197, 148, 65, 255)), (109, (222, 197, 139, 255)), (45, (139, 90, 32, 255)), (30, (90, 57, 8, 255)), (16, (148, 98, 98, 255)), (1, (205, 131, 32, 255))]



9.png
(530, (32, 98, 172, 255))
(433, (90, 139, 205, 255))
(177, (8, 57, 98, 255))
(41, (205, 205, 213, 255))
(20, (148, 172, 230, 255))

(290, (213, 172, 74, 255))
(269, (246, 213, 156, 255))
(213, (90, 57, 24, 255))
(87, (139, 98, 65, 255))
(31, (197, 74, 24, 255))

2
[(530, (32, 98, 172, 255)), (433, (90, 139, 205, 255)), (177, (8, 57, 98, 255)), (41, (205, 205, 213, 255)), (20, (148, 172, 230, 255))]
[(290, (213, 172, 74, 255)), (269, (246, 213, 156, 255)), (213, (90, 57, 24, 255)), (87, (139, 98, 65, 255)), (31, (197, 74, 24, 255))]










































"""

