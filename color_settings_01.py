# --- IMPORT --- #
import os
import time
import random
from tkinter import ttk
from tkinter import *
from configparser import ConfigParser
from tkinter.colorchooser import askcolor

"""

"""

# --- Config --- #
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)

# Color
color_settings = config["color_settings"]

BACKGROUND_COLOR = color_settings["bg_color"]
BUTTON_BG = color_settings["button_color"]
BUTTON_HOVER = color_settings["button_color_hover"]

# --- Variables --- #
bg_color = BACKGROUND_COLOR
but_col = BUTTON_BG
but_hov_col = BUTTON_HOVER


# --- Functions --- #
def save():
    global color_set
    color_set.destroy()

    config = ConfigParser()
    config["color_settings"] = {"bg_color" : bg_color,
                                "button_color" : but_col,
                                "button_color_hover" : but_hov_col}
    with open('config.ini', 'w') as configfile:
      config.write(configfile)



def change_bg_color():
    global bg_color_label
    global bg_color
    colors = askcolor(bg_color, title="Choose Color")
    bg_color = colors[1]
    txt_col = "black"
    if colors[0] < (100,100,100):
        txt_col = "white"
    bg_color_label.configure(bg=bg_color, fg=txt_col)

def change_but_color():
    global but_color_label
    global but_col
    colors = askcolor(but_col, title="Choose Color")
    but_col = colors[1]
    txt_col = "black"
    if colors[0] < (100,100,100):
        txt_col = "white"
    but_color_label.configure(bg=but_col, fg=txt_col)

def change_but_hov_color():
    global but_hov_color_label
    global but_hov_col
    colors = askcolor(but_hov_col, title="Choose Color")
    but_hov_col = colors[1]
    txt_col = "black"
    if colors[0] < (100,100,100):
        txt_col = "white"
    but_hov_color_label.configure(bg=but_hov_col, fg=txt_col)


# --- INIT --- #
color_set = Tk()
color_set.title("Color Settings")
color_set.geometry("800x800")
color_set.configure(bg=BACKGROUND_COLOR)

# BG Color
bg = LabelFrame(color_set, bg=BACKGROUND_COLOR)
bg.grid(row=0)
bg_color_label_frame = LabelFrame(bg, bg=BACKGROUND_COLOR, borderwidth=3)
bg_color_label_frame.grid(row=0, column=0)
bg_color_label = Label(bg_color_label_frame, text="Background Color", width=25, height=12, bg=BACKGROUND_COLOR)
bg_color_label.pack()
bg_picker = Button(bg, text="Pick Color", command=change_bg_color, activebackground=BUTTON_HOVER, bg=BUTTON_BG, height= 5, width=10)
bg_picker.grid(row=0, column=1, padx=15)

# Button Color
but = LabelFrame(color_set, bg=BACKGROUND_COLOR)
but.grid(row=1)
but_color_label_frame = LabelFrame(but, bg=BACKGROUND_COLOR, borderwidth=3)
but_color_label_frame.grid(row=0, column=0)
but_color_label = Label(but_color_label_frame, text="Primary Button Color", width=25, height=12, bg=BUTTON_BG)
but_color_label.pack()
but_picker = Button(but, text="Pick Color", command=change_but_color, activebackground=BUTTON_HOVER, bg=BUTTON_BG, height= 5, width=10)
but_picker.grid(row=0, column=1, padx=15)

#Button Hover Color
but_hov = LabelFrame(color_set, bg=BACKGROUND_COLOR)
but_hov.grid(row=2)
but_hov_color_label_frame = LabelFrame(but_hov, bg=BACKGROUND_COLOR, borderwidth=3)
but_hov_color_label_frame.grid(row=0, column=0)
but_hov_color_label = Label(but_hov_color_label_frame, text="Secondary Button Color", width=25, height=12, bg=BUTTON_HOVER)
but_hov_color_label.pack()
but_hov_picker = Button(but_hov, text="Pick Color", command=change_but_hov_color, activebackground=BUTTON_HOVER, bg=BUTTON_BG, height= 5, width=10)
but_hov_picker.grid(row=0, column=1, padx=15)

button_save = Button(color_set, text="save", command=save, bg=BUTTON_BG, activebackground=BUTTON_HOVER)
button_save.grid(row=5)

"""
dict = {}
dict[0] = but_color_label
dict[1] = but_hov_color_label
dict[0].configure(bg="green")
dict[1].configure(fg="red")
"""

# --- TK Mainloop --- #
color_set.mainloop()
