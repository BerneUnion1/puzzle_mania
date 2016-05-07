#!/usr/bin/env python

import os
import time
import argparse
from PIL import Image, ImageOps
from multiprocessing import Pool

DEBUG = False
SLICE_SIZE = 32
IN_DIR = ""
OUT_DIR = ""

def resize_pic(in_name):
    """Resize given image to square with slice_size:slice_size"""
    img = Image.open(in_name)
    img = ImageOps.fit(img, (SLICE_SIZE, SLICE_SIZE), Image.ANTIALIAS)
    return img


def get_average_color(img):
    """Calculate average color of given image"""
    width, height = img.size
    pixels = img.load()
    data = []
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            data.append(cpixel)
    r = 0
    g = 0
    b = 0
    counter = 0

    for x in range(len(data)):
        r += data[x][0]
        g += data[x][1]
        b += data[x][2]
        counter += 1

        rAvg = r / counter
        gAvg = g / counter
        bAvg = b / counter
        return (rAvg, gAvg, bAvg)


def get_image_paths():
    paths = []
    for file_ in os.listdir(IN_DIR):
        if DEBUG:
            print(file_)
        paths.append(IN_DIR + file_)    
    return paths 


def convert_image(path):
    img = resize_pic(path)
    color = get_average_color(img)
    img.save(str(OUT_DIR) + str(color) + ".jpg")


def convert_all_images():
    paths = get_image_paths()
    pool = Pool()
    pool.map(convert_image, paths)
    pool.close()
    pool.join()


def update_img_db():
    if DEBUG:
        print("Updating image database...")
    convert_all_images()


def find_closiest(color, list_colors):
    diff = 10000
    cur_closiest = 0
    for cur_color in list_colors:
        n_diff = abs(color[0] - cur_color[0]) + abs(color[1] - cur_color[1]) + abs(color[2] -cur_color[2])
        if n_diff < diff:
            diff = n_diff
            cur_closiest = cur_color
    return cur_closiest



def make_puzzle(img, color_list):
    width, heigth = img.size
    if DEBUG:
        print("Width = {}, Heigth = {}".format(width,heigth))
    # create white background 
    background = Image.new('RGB', img.size, (255,255,255))
    # go throught source image and construct final image
    total_images = 0
    if DEBUG:
        print("Start pasting images...\nImages pasted:")
    for y1 in range(0, heigth, SLICE_SIZE):
        for x1 in range(0, width, SLICE_SIZE):
            y2 = y1 + SLICE_SIZE
            x2 = x1 + SLICE_SIZE
            # crop needed part of source image
            new_img = img.crop((x1, y1, x2, y2))
            # get average color 
            color = get_average_color(new_img)
            close_img_name = find_closiest(color, color_list)
            close_img_name = OUT_DIR + str(close_img_name) + '.jpg'
            paste_img = Image.open(close_img_name)
            total_images += 1
            print("%s images \r" % total_images),
            background.paste(paste_img, (x1, y1))
    if DEBUG:
        print("Saving final image...")
    background.save('out.jpg')


def read_img_db():
    img_db = []
    for file_ in os.listdir(OUT_DIR):
        if DEBUG:
            print(file_)
        file_ = file_.split('.jpg')[0]
        file_ = tuple(map(int, file_[1:-1].split(',')))
        img_db.append(file_)
    return img_db


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", type=str, required=True,
                       help='input image')
    parser.add_argument("-d", "--directory", type=str, required=True,
                       help="source directory")
    parser.add_argument("-o", "--out", type=str, required=True,
                       help="out directory for cropped images")
    parser.add_argument("-s", "--size", type=int, required=False,
                       help="slice size")

    parser.add_argument("--update", help="update images", action="store_true")
    parser.add_argument("--debug", help="turn debug", action="store_true")
    
    args = parser.parse_args()

    start_time = time.time()

    if args.image:
        image = args.image

    if args.debug:
        DEBUG = True

    if args.directory:
        IN_DIR = args.directory
        print("IN_DIR: " + IN_DIR)
    if args.out:
        OUT_DIR = args.out
        print("OUT_DIR: " + OUT_DIR)

    if args.size:
        SLICE_SIZE = args.size
        print("Slice size: " + str(SLICE_SIZE))

    if args.update:
        list_of_imgs = read_img_db()
    else:
        update_img_db()
        list_of_imgs = read_img_db()

    img = Image.open(image)
    make_puzzle(img, list_of_imgs)

    print("Time: %s" % (time.time() - start_time))

    print("Done!")
