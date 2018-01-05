#! python3

import os, sys, os.path

# This appends the directory of the file to system path
# Prevents Import Error when double clicking .py file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from PIL import Image
import PIL.ImageOps

# Todo: Make user friendly. Prompt for current directory, if answer is no then prompt for path to run from

# Todo: Fill out Readme with information below:
# May not work on network locations, copy images to local drive before running
# Either place color_invert.py into the directory with your images or run it from command line
# If placing directly in the folder with images, can launch by double clicking. Answer Y to the first prompt about launching from the working directory
# If running from the command line, run with python 3, and answer N to the first prompt about working directory,
# then give the path to your images folder as an argument to the second prompt

def invert_colors(path, exclude):
    """Given a folder, inverts all .jpg and .png images in base and subfolders"""

    count_rgba = 0  #counts inverted RGBA images
    count_std = 0   #counts inverted standard images

    for dirpath, dirnames, filenames in os.walk(path, topdown=True):  #Walk through subdirectories of given path
        dirnames[:] = [d for d in dirnames if d not in exclude]
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

    exclude_list = []

    # determine whether script is run from image directory or not
    launch_choice = str(
        input("Are you running color_invert.py from the directory with the images you want to invert? (Y/n): ")).lower()

    # if answer is not y, n, or exit, try again
    if launch_choice != 'y' and launch_choice != 'n' and launch_choice != 'exit':
        print("Please only answer Y or n or type exit to quit")
        launch_choices()
        return

    elif launch_choice == 'exit':
        return


    exc_choice = str(input("Do you want to exclude any subfolders? (Y/n): ")).lower()

    # prompts for folders to exclude
    if exc_choice == 'y':
        print("\nType 'exit' or press Enter when you have listed all folders to be excluded")
        exc = str(input("Enter subfolder name to exclude (caps-sensitive): "))
        while exc.lower() != 'exit' and exc:
            exclude_list.append(exc)
            exc = str(input("Enter subfolder name to exclude (caps-sensitive): "))
        print("These are the folders you have chosen to exclude:")
        print(exclude_list)

    if launch_choice == 'y':
        print(invert_colors(os.getcwd(), exclude_list))

    elif launch_choice == 'n':
        print(invert_colors(cmd_launch(), exclude_list))

    elif launch_choice == 'exit':
        print("Exiting program...")



def main():
    path = ''                       # Avoid IOError if no path given, this will be caught with if statement below
    print("Welcome to Color Invert, you can find the latest version and documentation at https://github.com/rwesterman/color_invert")
    launch_choices()


if __name__ == '__main__':
    main()


