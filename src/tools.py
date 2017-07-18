from typing import List, Tuple

import os

from PIL import Image
import pygame as pg

from . import const
from . components import util


# XXX Unused
def strip_png(img):
    r, g, b, a = img.split()
    img = Image.merge("RGB", (r, g, b))
    return img


# XXX Unused
def convert_png(name_path, convert_to_ext=".bmp"):
    # Name here should include the extension
    original_name = name_path
    if os.path.exists(original_name):
        img = Image.open(original_name)

        name, ext = os.path.splitext(original_name)
        joined = name + convert_to_ext

        img = strip_png(img)

        img.save(joined)
        print(" ** Removing {} **".format(original_name))
        os.unlink(original_name)


def colorize(images: List[pg.Surface], color: Tuple[int, int, int]) -> List[pg.Surface]:
    colored = []
    for image in images:
        image = image.copy()
        #image.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
        image.fill(color + (0,), None, pg.BLEND_RGBA_ADD)
        colored.append(image)

    return colored


def recursive_load_gfx(path, accept=(".png", ".bmp", ".svg")):
    """
    Load graphics files.
    This operates on a one folder at a time basis.

    Note: An empty string doesn't count as invalid,
    since that represents a folder name.
    """
    colorkey = const.UGLY_PURPLE
    graphics = {}

    for pic in os.listdir(path):
        pic_path = os.path.join(path, pic)
        name, ext = os.path.splitext(pic)

        if ext.lower() in accept:
            img = pg.image.load(pic_path)

            if img.get_alpha():
                #img = img.convert_alpha()
                img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img

        elif not ext:
            pass
        else:
            print("Got unexpected gfx format\n" \
                    "Path: {}\n" \
                    "Name: {}\n" \
                    "Ext: {}\n".format(pic_path, name, ext))
    return graphics


def load_gfx(path):
    """Loads all the files in the graphics folder
    and also one more folder level deep.
    Doesn't recurse files deeper than that."""
    graphics = {}

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        name, ext = os.path.splitext(item)

        # If there is no extension, assume it's a folder.
        if ext == "":
            # WARNING: Update can overwrite existing keys
            graphics.update(recursive_load_gfx(item_path))
        else:
            graphics.update(recursive_load_gfx(path))

    # sanity check
    if not graphics:
        print("No graphics loaded.")

    return graphics


# Load all the fonts for all the sizes that I want to use.
def load_fonts(path, accept=(".ttf")):
    fonts = {}

    for pair in const.FONT_SIZE_DICT.items():
        font_size_name = pair[0] # Ex. menu, game, etc.
        font_size = pair[1]
        for font in os.listdir(path):
            name, ext = os.path.splitext(font)
            if ext.lower() in accept:
                # Add the intended size use to the name.
                name = "{}_{}".format(font_size_name, name)
                fonts[name] = pg.font.Font(os.path.join(path, font), font_size)
            else:
                print("Received invalid font. {}".format(font))

    return fonts


def load_sfx(path, accept=(".wav", ".mpe", ".ogg", ".mdi")):
    sounds = {}
    for sound in os.listdir(path):
        name, ext = os.path.splitext(sound)

        if ext.lower() in accept:
            sounds[name] = pg.mixer.Sound(os.path.join(path, sound))
        else:
            print("Received invalid sound effect. {}".format(sound))

    return sounds
