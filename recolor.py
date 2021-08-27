from PIL import Image
import os
from shutil import copyfile

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
        # show_colors(color_cluster)
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


def create_recolored_sprite(filename, colors):
    # copyfile("sprites/" + filename, "tests/" + filename)
    pass


def recolor_sprite(filename):
    print(filename)
    clusters = color_analysis(filename)
    create_recolored_sprite(filename, clusters)
    # print(len(clusters))
    #show_clusters(clusters)
    pass


def main():
    print(" ")
    with os.scandir("sprites") as it:
        for entry in it:
            if entry.name.endswith('.png') and entry.is_file():
                recolor_sprite(entry.name)
                



main()


"""

 
1.png
(218, (57, 148, 148, 255))
(133, (98, 213, 180, 255))
(67, (24, 74, 74, 255))
(36, (131, 238, 197, 255))
 
(88, (115, 172, 49, 255))
(52, (164, 213, 65, 255))
(35, (82, 98, 41, 255))
(22, (189, 255, 115, 255))
 
(14, (189, 41, 32, 255))
(6, (255, 106, 98, 255))
(4, (222, 74, 65, 255))
 
3
[(218, (57, 148, 148, 255)), (133, (98, 213, 180, 255)), (67, (24, 74, 74, 255)), (36, (131, 238, 197, 255))]
[(88, (115, 172, 49, 255)), (52, (164, 213, 65, 255)), (35, (82, 98, 41, 255)), (22, (189, 255, 115, 255))]  
[(14, (189, 41, 32, 255)), (6, (255, 106, 98, 255)), (4, (222, 74, 65, 255))]



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



3.png
(431, (32, 139, 115, 255))
(363, (82, 205, 172, 255))
(211, (131, 238, 222, 255))
(133, (16, 82, 65, 255))

(377, (255, 131, 115, 255))
(286, (222, 65, 65, 255))
(259, (131, 49, 0, 255))
(54, (189, 106, 49, 255))

(371, (57, 139, 41, 255))
(238, (106, 189, 74, 255))
(90, (148, 238, 148, 255))

(106, (255, 238, 82, 255))
(97, (222, 189, 41, 255))

4
[(431, (32, 139, 115, 255)), (363, (82, 205, 172, 255)), (211, (131, 238, 222, 255)), (133, (16, 82, 65, 255))]
[(377, (255, 131, 115, 255)), (286, (222, 65, 65, 255)), (259, (131, 49, 0, 255)), (54, (189, 106, 49, 255))]
[(371, (57, 139, 41, 255)), (238, (106, 189, 74, 255)), (90, (148, 238, 148, 255))]
[(106, (255, 238, 82, 255)), (97, (222, 189, 41, 255))]







"""

