[![codebeat badge](https://codebeat.co/badges/4d79217c-c0cd-4092-bf2f-169e5bbda1cc)](https://codebeat.co/projects/github-com-luminousmen-puzzle_mania)

# Puzzle mania

Using this script you will be able to create photographic mosaic from your pictures. 

### Requirements


  - Python 2.xxx
  - PIL

### Usage

First you need to current image database (even if doesn't exist yet). You need to specify input image, imgs for creating puzzle and directory to store cropped images. This command will create thumbnails of images and create output mozaic image:

```bash
$ ./puzzle.py -i ~/Pictures/in.jpg -o ~/Pictures/db/ -d ~/Pictures/imgs/ 

```

If you already ```update``` image database, for speeding up program you can create mozaic image without database update:

```bash
$ ./puzzle.py -i ~/Pictures/in2.jpg -o ~/Pictures/db/ -d ~/Pictures/imgs/ --update

```
You can specify slice size with ```-s``` option:
```bash
$ 
./puzzle.py -i ~/Pictures/in.jpg -o ~/Pictures/out/ -d ~/Pictures/imgs/ -s 16
```

### Examples
![in file2](/examples/in2.jpg)
![out file2](/examples/out2.jpg)

![in file](/examples/in.jpg)
![out file](/examples/out.jpg)
