from PIL import Image
import os
import colorsys
from PIL.ImagePalette import random
import numpy as np
import random

BLACK_COLOR = (16, 16, 16, 255)
PINK_COLOR = (255, 0, 255)

# 42.3 max
HUE_BOUND = 42


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
    red, green, blue = color[0], color[1], color[2]
    hue, _, _ = colorsys.rgb_to_hsv(red, green, blue)
    return truncate(hue)


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
    im = Image.open("tests/" + filename)
    colors = get_colors_from_image(im)
    # show_colors(colors)
    remove_alpha(colors)
    remove_grays(colors)
    clusters = get_clusters(colors)
    im.close()
    return clusters



# OLD
def recolor_cluster(color_cluster, recolor_hue):
    recolored_color_cluster = []
    """
    for color in color_cluster:
        old_rgb = color[1]
        new_rgb = update_rgb_by_hue(old_rgb, recolor_hue)
        recolored_color_cluster.append([color[0], new_rgb])
    """
    return recolored_color_cluster


def create_color_dict(color_cluster, recolor_hue):
    """
    color_cluster = color_clusters[0]
    show_colors(color_cluster)
    recolored_color_cluster = recolor_cluster(color_cluster, recolor_hue)
    show_colors(recolored_color_cluster)
    """
    color_dict = {}
    return color_dict


def generate_hue():
    # hue, _, _ = colorsys.rgb_to_hsv(227, 83, 154)
    hue = random.random() * 360
    return hue


def create_recolored_sprite(filename: str, color_clusters: list):
    # copyfile("sprites/" + filename, "tests/" + filename)
    im = Image.open("tests/" + filename) 
    recolor_hue = generate_hue()
    color_dict = create_color_dict(color_clusters, recolor_hue)
    for x in range(0, im.width):
        for y in range(0, im.width):
            old_color = im.getpixel((x,y))
            new_color = color_dict.get(old_color, PINK_COLOR)
            im.putpixel((x,y), new_color)
    im.close()


def recolor_sprite(filename):
    print(filename)
    # color_clusters = color_analysis(filename)
    # create_recolored_sprite(filename, color_clusters)
    # show_clusters(color_clusters)
    im = Image.open("tests/" + filename)

    im.close()


def main():
    print(" ")
    with os.scandir("tests") as it:
        for entry in it:
            if entry.name.endswith('.png') and entry.is_file():
                recolor_sprite(entry.name)
                

def apply_hue(rgb, hue):
    red, green, blue = rgb
    _, saturation, value = colorsys.rgb_to_hsv(red, green, blue)
    red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
    return truncate(red), truncate(green), truncate(blue)


def test():
    im = Image.open('tests/3.png')
    im = im.convert('RGBA')
    data = np.array(im)   # "data" is a height x width x 4 numpy array
    im.close()

    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
    hue = generate_hue()

    color_a = (32, 139, 115)
    color_b = (82, 205, 172)
    color_c = (131, 238, 222)
    color_d = (16, 82, 65)    

    color_a_mask = (red == 32)  & (green == 139) & (blue == 115)
    color_b_mask = (red == 82)  & (green == 205) & (blue == 172)
    color_c_mask = (red == 131) & (green == 238) & (blue == 222)
    color_d_mask = (red == 16)  & (green == 82 ) & (blue == 65 )

    color_a = apply_hue(color_a, hue)
    color_b = apply_hue(color_b, hue)
    color_c = apply_hue(color_c, hue)
    color_d = apply_hue(color_d, hue)

    data[..., :-1][color_a_mask.T] = color_a
    data[..., :-1][color_b_mask.T] = color_b
    data[..., :-1][color_c_mask.T] = color_c
    data[..., :-1][color_d_mask.T] = color_d
   
    im2 = Image.fromarray(data)
    im2.show()
  



test()

"""



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

