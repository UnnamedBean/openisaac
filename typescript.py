# import the stuffs
from pynput.mouse import Controller as MouseController
import keyboard
import pyautogui
from PIL import ImageGrab
import time

# define what "mouse" and "mousepos" are
mouse = MouseController()
mousepos = mouse.position                   

# Finds the mouse, wait for you to press enter and prints it
def findmouspos():
    return mouse.position

def get_pixel_color(x, y):
    screenshot = ImageGrab.grab()
    rgb_color = screenshot.getpixel((x, y))
    return rgb_color

print("Press Enter to Scan Mouse Location!")
keyboard.wait('enter')
mousepos = findmouspos()
rgb_color = get_pixel_color(mousepos[0], mousepos[1])

time.sleep(0.1)
print(f"The current mouse position is: {mousepos}")
print(f"The color underneath your mouse is: {rgb_color}")