from PIL import Image, ImageGrab, ImageChops
from pynput.mouse import Controller
import os.path
import datetime
import keyboard
import random
import time
import threading


def GetPathWithFileIndex(fpath):
    """
    Returns the path where the file should be saved.
    If ...\1.png already exists it returns ...\1_1.png.
    """
    if os.path.isfile(fpath):
        offset = 0
        while True:
            offset += 1
            new_fpath = fpath.split(".png")[0] + "_" + str(offset) + ".png"
            if os.path.isfile(new_fpath):
                continue
            else:
                return new_fpath
    else:
        return str(fpath)


def CreateDirectory(dpath):
    """
    Recursively creates the working directory.
    """
    if os.path.isdir(dpath) == False:
        try:
            os.makedirs(dpath, mode = 0o777)
        except OSError:
            print ("Creation of the directory %s failed" % dpath)
        else:
            print ("Successfully created the directory %s " % dpath)
    else:
        print("%s directory already exists" % dpath)


def PictureCompare(image1, image2):
    """
    Compares two images and returns true if images are the same.
    """
    return ImageChops.difference(image1, image2)


def main():
    working_dir = os.path.abspath(os.path.dirname(__file__))
    now = datetime.datetime.now()
    date = str(now.strftime("%m.%d.%y"))
    session = str(random.randint(0,999999))
    directory = "Diskrete Mathematik 2020"

    path_manual = os.path.join(working_dir, directory, date, "Manual", session)
    path_automatic = os.path.join(working_dir, directory, date, "Automatic", session)

    manualThead = threading.Thread(target=ManualScreenshot, args=(path_manual,"F8",))
    automaticThead = threading.Thread(target=AutoScreenshot, args=(path_automatic,2,"F9",))

    manualThead.start()
    automaticThead.start()


def ManualScreenshot(path, screenshot_key):
    """
    Saves a screenshot of the main monitor if a key is pressed (F8)
    """
    CreateDirectory(path)
    index = 0
    while True:
        if keyboard.is_pressed(str(screenshot_key)):
            print("Manual Thread: Took screenshot")
            file_path = GetPathWithFileIndex(os.path.join(path, str(index) + ".png"))
            screen = ImageGrab.grab()
            screen.save(file_path, "PNG")
            index +=1


def AutoScreenshot(path, screenshot_interval, pageindex_select_key):
    """
    User has to select the page number with pageindex_select_key.
    Takes a screenshot of the main monitor every few seconds (screenshot_interval),
    crops the screenshots to the script index and if the two screenshots
    are different, meaning it's a different page, it saves the older screenshot.
    """
    CreateDirectory(path)
    mouse = Controller()
    print("Move your mouse to the top left position of the page index and press {}".format(pageindex_select_key))
    while True:
        if keyboard.is_pressed(str(pageindex_select_key)):
            top_left_pos = mouse.position
            break

    time.sleep(1)
    print("Move your mouse to the bottom right position of the page index and press {}".format(pageindex_select_key))
    while True:
        if keyboard.is_pressed(str(pageindex_select_key)):
            bottom_right_pos = mouse.position
            break

    crop_factors = (top_left_pos[0], top_left_pos[1], bottom_right_pos[0], bottom_right_pos[1])
    print("Crop factors: " + str(crop_factors))
    index = 0
    temp2Screen = ImageGrab.grab()
    while True:
        print("\n")
        temp1Screen = temp2Screen
        print("Auto Thread: Took Screenshot 1")
        time.sleep(screenshot_interval)
        temp2Screen = ImageGrab.grab()
        print("Auto Thread: Took Screenshot 2")

        diff = PictureCompare(temp1Screen.crop(crop_factors), temp2Screen.crop(crop_factors))
        if diff.getbbox():
            print("Auto Thread: Images are different. Took screenshot")
            file_path = GetPathWithFileIndex(os.path.join(path, str(index) + ".png"))
            temp1Screen.save(file_path, "PNG")
            index +=1
        else:
            print("Auto Thread: Images are the same. No screenshot taken")


if __name__ == '__main__':
    main()
