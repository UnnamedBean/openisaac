from pynput.mouse import Controller as MouseController
from pynput.mouse import Controller as MouseController, Button
from PIL import Image
import pyautogui
import keyboard
import time

mouse = MouseController()
mousepos = mouse.position
originalmousepos = mouse.position

def ogmousepos():
    return originalmousepos

mouse.position = (1478, 1413)
mouse.click(Button.left)
print('Isaac Opened')

time.sleep(13)
print("isaac loaded")

screenshot = pyautogui.screenshot()
pixel_color = screenshot.getpixel((170, 882))

target_color = (158, 115, 45)

if pixel_color == target_color:
    keyboard.press('space')
else:
    print("not isaac d:")