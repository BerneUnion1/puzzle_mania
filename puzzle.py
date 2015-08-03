from PIL import Image, ImageOps
import sys
import os

slice_size = 32

in_dir = '/home/kir/Projects/python/puzzle/in_img/'
out_dir = '/home/kir/Projects/python/puzzle/out_img/'

def resize_pic(in_name):
    img = Image.open(in_name)
    img = ImageOps.fit(img, (slice_size, slice_size), Image.ANTIALIAS)
    return img

def get_average_color(img):
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

        rAvg = r/counter
        gAvg = g/counter
        bAvg = b/counter
        return (rAvg, gAvg, bAvg)

def convert_all_images(in_dir, out_dir, list_of_imgs):
    for file_ in os.listdir(in_dir):
        print(file_)
        img = resize_pic(in_dir + file_)
        color = get_average_color(img)
        img.save(str(out_dir) + str(color) + ".jpg")
        list_of_imgs.append(color)

def find_closiest(color, out_dir, list_colors):
    diff = 10000
    cur_closiest = 0
    for cur_color in list_colors:
        n_diff = abs(color[0] - cur_color[0]) + abs(color[1] - cur_color[1]) + abs(color[2] -cur_color[2])
        if n_diff < diff:
            diff = n_diff
            cur_closiest = cur_color
    return cur_closiest

def do_the_thing(img, out_dir, color_list):
    width, heigth = img.size
    background = Image.new('RGB', img.size, (255,255,255))
    for y1 in range(0, heigth, slice_size):
        for x1 in range(0, width, slice_size):
            y2 = y1 + slice_size
            x2 = x1 + slice_size
            new_img = img.crop((x1,y1,x2,y2))
            curr_color = get_average_color(new_img)
            close_img_name = find_closiest(curr_color, out_dir, color_list)
            close_img_name = out_dir + str(close_img_name) + '.jpg'
            paste_img = Image.open(close_img_name)

            background.paste(paste_img, (x1, y1))
    background.save('out.jpg')

if __name__ == '__main__':
    DO_IT = True
    list_of_imgs = []
    if DO_IT == True:
        convert_all_images(in_dir, out_dir, list_of_imgs)
    in_image = '/home/kir/Projects/python/puzzle/in2.jpg'
    img = Image.open(in_image)
    do_the_thing(img, out_dir, list_of_imgs)


