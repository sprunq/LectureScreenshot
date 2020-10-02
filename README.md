
# LectureScreenshot
A simple script for making automatic/manual screenshots of my Zoom lecture every time the slide changes or a button (F8) is pressed. 
This script saves every screenshot as a png in a session subfolder, which is randomly determined at startup, in the date subfolder. 
Compile the script screenshots into one pdf with applications like Gimp.

## Important:
Default screenshot button is F8 but feel free to change it in the source code.
The values in the automatic function are set to crop with a 1440p 16:9 screen with Zoom in fullscreen and chat and participant list extended.
If you have a different resolution calculate or try to find it yourself. 

## Setup:
Install Python and run these commands in the console: 
```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
python3 -m pip install --upgrade keyboard
```
