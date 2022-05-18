import ntpath
from PIL import Image
import os
import colorsys
from PIL.ImagePalette import random
import numpy as np
import random
import time

BLACK_COLOR = (16, 16, 16, 255)

PINK_COLOR = (255, 0, 255)


HUE_BOUND = 0.1


def get_main_color(colors):
    if (colors[0][1] == BLACK_COLOR):
        main_color = colors[1][1]
    else:
        main_color = colors[0][1]
    return main_color


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


def truncate(value, decimals=4):
    return int(value*(10**decimals))/(10**decimals)


def get_hue(color):
    red, green, blue = color[0], color[1], color[2]
    hue, _, _ = colorsys.rgb_to_hsv(red, green, blue)
    return truncate(hue)


def hue_delta(hua_a, hue_b):
    delta = abs(hua_a - hue_b)
    if ( delta > 180 ):
        delta = 360 - delta
    return truncate(delta)


def get_color_cluster(colors:list):
    color_cluster = []
    cluster_size = 0
    main_color = get_main_color(colors)
    main_hue = get_hue(main_color)
    for color in list(colors):
        hue = get_hue(color[1])
        delta_hue = hue_delta(main_hue, hue)
        if delta_hue < HUE_BOUND:
            # print(main_color, color[1], "[[[", delta_hue, "]]]")
            color_cluster.append(color)
            cluster_size += 1
            colors.remove(color)
        # else:
            # print(main_color, color[1], delta_hue)
    return color_cluster, cluster_size


def generate_hue()->float:
    hue = random.random()
    return hue


def generate_color_clusters(colors:list):
    clusters = []
    amount_colors = len(colors)
    while(amount_colors > 0):
        color_cluster, cluster_size = get_color_cluster(colors)
        amount_colors = amount_colors - cluster_size
        clusters.append(color_cluster)
    return clusters


def show_clusters(clusters:list):
    for cluster in clusters:
        print(cluster)


def apply_hue(old_rgb, hue):
    old_red, old_green, old_blue = old_rgb
    _, saturation, value = colorsys.rgb_to_hsv(old_red, old_green, old_blue)
    new_red, new_green, new_blue = colorsys.hsv_to_rgb(hue, saturation, value)
    new_rgb = int(new_red), int(new_green), int(new_blue)
    new_rgb = PINK_COLOR
    return new_rgb


def generate_color_masks(color_cluster, data):
    red, green, blue, _ = data.T
    color_masks = []
    for color in color_cluster:
        color_mask = (red == color[0]) & (green == color[1]) & (blue == color[2])
        color_masks.append(color_mask)
    return color_masks


def update_color_cluster(old_color_cluster, hue):
    new_color_cluster = []
    for old_color in old_color_cluster:
        new_color = apply_hue(old_color, hue)
        new_color_cluster.append(new_color)
    return new_color_cluster


def update_data(data, color_cluster, color_masks):
    for color, color_mask in zip(color_cluster, color_masks):
        data[..., :-1][color_mask.T] = color
    return data


def format_color_cluster(old_color_cluster):
    new_color_cluster = []
    for old_color in old_color_cluster:
        new_color = old_color[1][0:3]
        new_color_cluster.append(new_color)
    return new_color_cluster


def format_color_clusters(old_color_clusters:list):
    new_color_clusters = []
    for old_color_cluster in old_color_clusters:
        new_color_cluster = format_color_cluster(old_color_cluster)
        new_color_clusters.append(new_color_cluster)
    return new_color_clusters


def color_amount(elem):
    return elem[0]


def get_colors_from_image(image:Image.Image):
    colors = image.getcolors()
    colors.sort(key=color_amount, reverse=True)
    return colors


def get_color_clusters(im:Image.Image):
    colors = get_colors_from_image(im)
    remove_alpha(colors)
    remove_grays(colors)
    color_clusters = generate_color_clusters(colors)
    color_clusters = format_color_clusters(color_clusters)
    return color_clusters


def get_image(filename: str):
    sprite_path = os.path.join("sprites", filename)
    image = Image.open(sprite_path)
    image = image.convert('RGBA')
    return image


def recolor_sprite(file: os.DirEntry):
    filename = file.name
    print(filename)

    current_image = get_image(filename)
    data = np.array(current_image)
    color_clusters = get_color_clusters(current_image)

    # TODO : make one sprite per color cluster of each pokemon
    # color_clusters = [color_clusters[-1]]

    for old_color_cluster in color_clusters:
        hue = generate_hue()
        color_masks = generate_color_masks(old_color_cluster, data)
        new_color_cluster = update_color_cluster(old_color_cluster, hue)
        data = update_data(data, new_color_cluster, color_masks)
    current_image.close()

    new_image = Image.fromarray(data)
    result_path = os.path.join("results", filename)
    new_image.save(result_path)
    new_image.close()


def is_sprite(element: os.DirEntry):
    return element.name.endswith('.png') and element.is_file()


def recolor_sprites():
    with os.scandir("sprites") as elements:
        print(" ")
        for element in elements:
            if is_sprite(element):
                recolor_sprite(element)
        print(" ")

if __name__ == "__main__":
    recolor_sprites()
