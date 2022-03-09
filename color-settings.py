# --- IMPORT --- #
import os
import time
import random
from tkinter import ttk
from tkinter import *
from configparser import ConfigParser
from tkinter.colorchooser import askcolor



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
text_color = "black"

colors = {"Background Color":bg_color, "Text Color":text_color, "Primary Button Color":but_col, "Secondary Button Color":but_hov_col}
#colors = [[bg_color, "Background Color"], [but_col, "Primary Button Color"], [but_hov_col, "Secondary Button Color"], [text_color, "Text Color (WIP)"]]
color_elems = [] #[Elem, Elem, ...] Elem = [LabelFrame, ColorLabelFrame, ColorLabel, PickerButton, ColorName]




# --- Functions --- #
def save():
    global color_set
    color_set.destroy()

    config = ConfigParser()
    config["color_settings"] = {"bg_color" : colors["Background Color"],
                                "button_color" : colors["Primary Button Color"],
                                "button_color_hover" : colors["Secondary Button Color"],
                                "text_color" : colors["Text Color"]}
    with open('config.ini', 'w') as configfile:
      config.write(configfile)


def change_color(index):
    global color_elems
    global colors

    title = "Choose " + color_elems[index][4]

    color = askcolor(colors[color_elems[index][4]], title=title)

    color_elems[index][2].configure(bg=color[1])
    colors[color_elems[index][4]] = color[1]

    reload_colors()


def reload_colors():
    color_set.configure(bg = colors["Background Color"])
    button_save.configure(bg = colors["Primary Button Color"], activebackground=colors["Secondary Button Color"])
    colors_frame.configure(bg = colors["Background Color"])

    for elem in color_elems:
        elem[0].configure(bg = colors["Background Color"])
        elem[1].configure(bg = colors["Background Color"])
        elem[3].configure(bg = colors["Primary Button Color"], activebackground=colors["Secondary Button Color"])


# --- INIT --- #
color_set = Tk()
color_set.title("Color Settings")
color_set.geometry("800x800")
color_set.configure(bg=BACKGROUND_COLOR)
color_set.grid_rowconfigure(0, weight=0)
color_set.grid_columnconfigure(0, weight=1)

colors_frame = LabelFrame(color_set, bg=BACKGROUND_COLOR, borderwidth=0)
colors_frame.pack(pady=10)

i = 0
for color in colors:
    label_frame = LabelFrame(colors_frame, bg=BACKGROUND_COLOR, text=color)
    label_frame.grid(row=i//2+1, column=i % 2, padx=15, pady=15)
    color_label_frame = LabelFrame(label_frame, bg=BACKGROUND_COLOR, borderwidth=3)
    color_label_frame.grid(row=0, column=0)
    color_label = Label(color_label_frame, width=25, height=12, bg=colors[color])
    color_label.pack()
    picker_button = Button(label_frame, text="Pick Color", command=lambda i=i: change_color(i), activebackground=BUTTON_HOVER, bg=BUTTON_BG, height= 5, width=10)
    picker_button.grid(row=0, column=1, padx=15)

    color_elems += [[label_frame, color_label_frame, color_label, picker_button, color]]

    i += 1


button_save = Button(color_set, text="Save", command=save, bg=BUTTON_BG, activebackground=BUTTON_HOVER)
button_save.pack(pady=10)

"""
dict = {}
dict[0] = but_color_label
dict[1] = but_hov_color_label
dict[0].configure(bg="green")
dict[1].configure(fg="red")
"""

# --- TK Mainloop --- #
color_set.mainloop()
