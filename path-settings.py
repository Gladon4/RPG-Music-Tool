# --- IMPORT --- #
import os
import time
import random
from tkinter import ttk
from tkinter import *
import csv
from configparser import ConfigParser
import sys

# --- CONSTANTS --- #
BASE_PATH = os.path.dirname(__file__)

# --- Variables --- #


# --- Config --- #
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)

# Color
color_settings = config["color_settings"]

BACKGROUND_COLOR = color_settings["bg_color"]
BUTTON_BG = color_settings["button_color"]
BUTTON_HOVER = color_settings["button_color_hover"]
TEXT_COLOR = color_settings["text_color"]

paths = []
with open(BASE_PATH+"/paths.csv", "r", encoding="utf-8-sig") as csv_file:
    list = csv.reader(csv_file, delimiter=',', quotechar='|')
    for row in list:
        paths = row


# --- Functions --- #
def save_paths():
    # text_box.config(fg="red")
    new_paths = text_box.get(1.0, 'end').split()
    text_box.delete(1.0, 'end')

    new_text = []

    for path in new_paths:
        try:
            with open(path + "/songs.csv") as file:
                new_text += [(path, True)]

        except:
            try:
                songs = open(path + "/songs.csv", 'a')
                songs.close()
                new_text += [(path, True)]

            except:
                new_text += [(path, False)]

    for i in new_text:
        if i[1]:
            text_box.insert('end', i[0] + "\n", None)
        else:
            text_box.insert('end', i[0] + "\n", "warning")

    with open(BASE_PATH+"/paths.csv", "w") as csv_file:
        write = csv.writer(csv_file)
        write.writerow(new_paths)

    # path_set.destroy()

# --- INIT --- #
path_set = Tk()
path_set.title("Song Settings")
path_set.geometry("400x400")
path_set.configure(bg=BACKGROUND_COLOR)
path_set.grid_rowconfigure(0, weight=0)
path_set.grid_columnconfigure(0, weight=1)


paths_text = ""
for p in paths:
    paths_text += p + "\n"

label_title = Label(path_set, text="Configure Paths",font=("Helvetica",18), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
label_title.pack()

text_box = Text(path_set, height=18, width=40, bg=BACKGROUND_COLOR, fg=TEXT_COLOR,borderwidth=0)
text_box.pack()
text_box.insert('end', paths_text)
text_box.config(state='normal')
text_box.tag_configure("warning", foreground="red")


save_button = Button(path_set, text="Save Paths", command=save_paths, borderwidth=0,activebackground=BUTTON_HOVER, bg=BUTTON_BG, fg=TEXT_COLOR, height=2, width=8)
save_button.pack()


path_set.mainloop()
