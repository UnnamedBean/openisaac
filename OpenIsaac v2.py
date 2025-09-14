# OpenIsaac v.2
from pynput.mouse import Controller as MouseController, Button
from PIL import Image
import pyautogui
import keyboard
import os
import tkinter as tk
from tkinter import messagebox
import os, sys

if getattr(sys, 'frozen', False):  # running as exe
    base_path = os.path.dirname(sys.executable)
else:  # running as .py
    base_path = os.path.dirname(os.path.abspath(__file__))

pos_file = os.path.join(base_path, "data.txt")


mouse = MouseController()
mousepos = mouse.position

def save_mousepos(position):
    with open(pos_file, "w") as f:
        f.write(f"{position[0]},{position[1]}")

def load_mousepos():
    if not os.path.exists(pos_file):
        return None
    with open(pos_file, "r") as f:
        x, y = f.read().strip().split(",")
        return (int(x), int(y))

def ask_continue_or_exit():
    choice = messagebox.askyesno("OpenIsaac", "Would you like to Continue?")
    return "Yes" if choice else "No"

def ask_yes_or_no():
    choice = messagebox.askyesno("OpenIsaac", "Y / N?")
    return "Yes" if choice else "No"

def start_automation(mousepos):
    mouse.position = mousepos
    mouse.click(Button.left)
    print_to_box('Opened')
    root.after(13000, check_pixel)

def check_pixel():
    screenshot = pyautogui.screenshot()
    pixel_color = screenshot.getpixel((170, 882))
    target_color = (158, 115, 45)
    if pixel_color == target_color:
        print_to_box("Ooooh, Isaac :D")
        root.after(2000, lambda: keyboard.press_and_release('space'))
        root.after(2000, lambda: print_to_box("Pressed space!"))
    else:
        print_to_box("Not Isaac d:")
    root.after(4500, lambda: print_to_box("Automation complete."))

def get_mouse_position_gui():
    pos = {}
    top = tk.Toplevel(root)  # Keep main window
    top.title("Save Mouse Position")
    top.geometry("400x150")

    tk.Label(top, text="Hover over the app and press SPACE to save the mouse position.").pack(pady=10)

    def save_pos(event=None):  # event is needed for key bindings
        pos['value'] = mouse.position
        top.destroy()

    # Bind the spacebar key to save_pos
    top.bind('<space>', save_pos)

    top.grab_set()
    top.wait_window()
    return pos['value']

root = tk.Tk()
root.title("OpenIsaac")
root.geometry("600x400")
tk.Label(root, text="Welcome To OpenIsaac Version 2.0.9").pack(pady=10)

def on_close():
    # Cancel all scheduled tasks and quit
    root.quit()  # safely stop mainloop

root.protocol("WM_DELETE_WINDOW", on_close)

text_box = tk.Text(root, height=20, width=70)
text_box.pack(pady=10)

def print_to_box(msg):
    if text_box.winfo_exists():   # check if widget still exists
        text_box.config(state=tk.NORMAL)
        text_box.insert(tk.END, msg + "\n")
        text_box.see(tk.END)
        text_box.config(state=tk.DISABLED)

def save_mouse_position():
    global saved_position
    saved_position = mouse.position
    print_to_box(f"Mouse position saved at {saved_position}")

def on_close():
    keyboard.unhook_all()  # stop global hotkeys
    root.quit()

keyboard.add_hotkey('space', save_mouse_position)  # add once at start

def run_openisaac():
    global mousepos
    mousepos = load_mousepos()

    if mousepos is None:
        print_to_box("No saved position found. Press SPACE over target app to save.")
        wait_for_saved_position()
    else:
        print_to_box(f"Using saved position {mousepos}")
        root.after(800, lambda: start_automation(mousepos))

def wait_for_saved_position():
    if 'saved_position' in globals():
        save_mousepos(saved_position)
        check_user_continue(saved_position)
    else:
        root.after(500, wait_for_saved_position)


def check_user_continue(mousepos):
    choice = ask_continue_or_exit()
    if choice == "Yes":
        print_to_box("Loading...")
        root.after(800, lambda: start_automation(mousepos))
    else:
        retry = ask_yes_or_no()
        if retry == "No":
            print_to_box("Retrying!")
            root.after(100, lambda: run_openisaac())
        else:
            print_to_box("Goodbye!")
            root.after(800, root.quit)

root.after(100, run_openisaac)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()