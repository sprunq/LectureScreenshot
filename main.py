from PIL import Image, ImageGrab
import os.path
import datetime
import keyboard
import random

def checkIfFileExists(fpath):
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


def createDirectory(dpath):
    # Recursively creates the working directory
    if os.path.isdir(dpath) == False:
        try:
            os.makedirs(dpath, mode = 0o777)
        except OSError:
            print ("Creation of the directory %s failed" % dpath)
        else:
            print ("Successfully created the directory %s " % dpath)
    else:
        print("%s directory already exists" % dpath)


def main():
    working_dir = os.path.abspath(os.path.dirname(__file__))
    directory = "Diskrete Mathematik 2020"
    now = datetime.datetime.now()
    date = str(now.strftime("%m.%d.%y"))
    session = str(random.randint(0,999999))
    path = os.path.join(working_dir, directory, date, session)

    # Create directory
    createDirectory(path)

    # Check for keypress
    index = 0
    while True:
        if keyboard.is_pressed('F8'):
            file_path = checkIfFileExists(os.path.join(path, str(index) + ".png"))
            screen = ImageGrab.grab()
            screen.save(file_path, "PNG")
            index +=1


if __name__ == '__main__':
    main()
