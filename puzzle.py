from PIL import Image, ImageOps
import sys
import os

slice_size = 24
in_dir = '/home/kir/Projects/python/puzzle/in_img/'
out_dir = '/home/kir/Projects/python/puzzle/out_img/'

def resize_pic(in_name):
    """Resize given image to square with slice_size:slice_size"""
    img = Image.open(in_name)
    img = ImageOps.fit(img, (slice_size, slice_size), Image.ANTIALIAS)
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

def convert_all_images(in_dir, out_dir, list_of_imgs):
    for file_ in os.listdir(in_dir):
        if DEBUG:
            print(file_)
        img = resize_pic(in_dir + file_)
        color = get_average_color(img)
        img.save(str(out_dir) + str(color) + ".jpg")
        list_of_imgs.append(color)

def update_img_db(in_dir, out_dir):
    if DEBUG:
        print("Updating image database...")
    img_db = []
    convert_all_images(in_dir, out_dir, img_db)
    return img_db

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
    if DEBUG:
        print("Width = {}, Heigth = {}".format(width,heigth))
    #create white background 
    background = Image.new('RGB', img.size, (255,255,255))
    #go throught source image and construct final image
    total_images = 0
    print("Start pasting images...\n Images pasted:")
    for y1 in range(0, heigth, slice_size):
        for x1 in range(0, width, slice_size):
            y2 = y1 + slice_size
            x2 = x1 + slice_size
            #crop needed part of source image to get color
            new_img = img.crop((x1,y1,x2,y2))
            curr_color = get_average_color(new_img)
            close_img_name = find_closiest(curr_color, out_dir, color_list)
            close_img_name = out_dir + str(close_img_name) + '.jpg'
            paste_img = Image.open(close_img_name)
            total_images += 1
            print("%s images \r" % total_images),
            background.paste(paste_img, (x1, y1))
    if DEBUG:
        print("Saving final image...")
    background.save('out.jpg')

def read_img_db(in_dir):
    img_db = []
    for file_ in os.listdir(in_dir):
        if DEBUG:
            print(file_)
        file_ = file_.split('.jpg')[0]
        file_ = tuple(map(int, file_[1:-1].split(',')))
        img_db.append(file_)
    return img_db

if __name__ == '__main__':
    DEBUG = True
    DO_IT = False
    if "update" in sys.argv[1:]:
        list_of_imgs = update_img_db(in_dir, out_dir)
    else:
        list_of_imgs = read_img_db(out_dir)
    in_image = '/home/kir/Projects/python/puzzle/in2.jpg'
    img = Image.open(in_image)
    do_the_thing(img, out_dir, list_of_imgs)
    print("\nDone!")
    
