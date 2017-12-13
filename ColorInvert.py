#! Python3

from PIL import Image
import PIL.ImageOps
import os, sys, os.path

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



path = ''                       # Avoid IOError if no path given, this will be caught with if statement below

try:
    path = sys.argv[1]          #Takes first argument after script name as path
except IndexError as e:
    print("Index error. No target path found")  #Catches index error if it occurs

if path.lower() == 'help' or not path:
    print("Please provide a path to your images as an argument after the script path")
    print("Eg. python c:/ColorInvert.py c:/images")



else:
    try:
        print(invert_colors(path))
    except OSError as e:
        print("Error: given path does not exist")
