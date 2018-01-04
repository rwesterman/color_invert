#! /usr/bin/env python3

import os, sys, os.path
from PIL import Image
import PIL.ImageOps

def invert_colors(path):
    """Given a folder, inverts all .jpg and .png images in base and subfolders"""

    count_rgba = 0  #counts inverted RGBA images
    count_std = 0   #counts inverted standard images

    for dirpath, dirnames, filenames in os.walk(path):  #Walk through subdirectories of given path
        for file in filenames:
            if ".png" in file or ".jpg" in file:
                fullpath = os.path.join(dirpath, file)  #Take full path name to each image
                image = Image.open(fullpath)            #Open image

                if image.mode == 'RGBA':                #This is only for RGBA type images
                    r,g,b,a = image.split()
                    rgb_image = Image.merge('RGB', (r,g,b))
                    inverted_image = PIL.ImageOps.invert(rgb_image)
                    r2,g2,b2 = inverted_image.split()
                    final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
                    final_transparent_image.save(fullpath)
                    count_rgba = count_rgba + 1

                else:
                    inverted_image = PIL.ImageOps.invert(image)
                    inverted_image.save(fullpath)
                    count_std = count_std + 1

    return("Inverted {} RGBA images, and {} standard images".format(count_rgba, count_std))

def cmd_launch():

    try:
        path = input("Please enter the full filepath to a directory containing the images to be inverted:")
    except IndexError as e:
        print("Index error. No target path found")  #Catches index error if it occurs
    return path


def launch_choices():

    # determine whether script is run from image directory or not
    launch_choice = str(
        input("Are you running color_invert.py from the directory with the images you want to invert? (Y/n)")).lower()

    # Invert images in working directory
    if launch_choice == 'y':
        print(invert_colors(os.getcwd()))

    # Send to cmd_launch to prompt user for filepath
    elif launch_choice == 'n':
        print(invert_colors(cmd_launch()))

    # Give user the option to exit without inverting
    elif launch_choice == 'exit':
        print("Exiting program...")

    # if answer is not y, n, or exit, try again
    else:
        print("Please only answer Y or n or type exit to quit")
        launch_choices()

def main():
    path = ''                       # Avoid IOError if no path given, this will be caught with if statement below
    print("Welcome to Color Invert, you can find the latest version and documentation at https://github.com/rwesterman/color_invert")
    launch_choices()


if __name__ == '__main__':
    main()


