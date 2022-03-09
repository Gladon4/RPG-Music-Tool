# --- IMPORT --- #
from mutagen.mp3 import MP3
import os
import time
import random
import pygame
from tkinter import ttk
from tkinter import *
import csv
from configparser import ConfigParser
from tkinter.colorchooser import askcolor


# --- CONSTANTS --- #
BASE_PATH = os.path.dirname(__file__)


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
global theme
global length
global stopped

themes = {}
first = True
paused = False
stopped = True


# --- Functions --- #
def change_theme(next_theme):
    global theme
    global stopped
    global paused

    stopped = False
    paused = False
    theme = next_theme
    next_song = get_next_song(next_theme)

    label_current_theme.config(text=next_theme)
    button_pause.config(image=pause_image)

    play(next_song)


def play(song):
    global length
    global first

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_mut = MP3(song)
    length = song_mut.info.length

    if BASE_PATH[1] == ":": # Windows
        song_name = song.split("\\")[len(song.split("\\")) - 1].split(".mp3")[0]
        label_current_song.config(text=song_name)

    else: # Linux
        song_name = song.split("/")[len(song.split("/")) - 1].split(".mp3")[0]
        label_current_song.config(text=song_name)

    if first:
        first = False
        song_duration()


def get_next_song(next_theme):
    song_id = random.randint(0, len(themes[next_theme]) - 1)
    song_path = themes[next_theme][song_id]
    return song_path


def song_duration():
    if not stopped:
        current_time = pygame.mixer.music.get_pos() / 1000
        converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
        converted_length = time.strftime('%M:%S', time.gmtime(length))
        song_time = str(converted_current_time) + " / " + str(converted_length)

        label_duration_song.config(text=song_time)
        song_progress['value'] = current_time / length * 100

        if current_time <= 0 and not stopped:
            song = get_next_song(theme)
            play(song)

    label_duration_song.after(1000, song_duration)


def pause():
    global paused
    if paused:
        paused = False
        button_pause.config(image=pause_image)
        pygame.mixer.music.unpause()
    else:
        paused = True
        button_pause.config(image=play_image)
        pygame.mixer.music.pause()


def stop():
    global stopped

    stopped = True
    pygame.mixer.music.stop()

    label_current_song.config(text="No Song Playing")
    label_current_theme.config(text="No Theme Selected")
    song_time = "00:00 / 00:00"
    label_duration_song.config(text=song_time)


def skip():
    if not stopped:
        song = get_next_song(theme)
        play(song)


def volume(pos):
    pygame.mixer.music.set_volume(float(pos) / 100)
    label_volume.config(text=str(int(float(pos))))


def open_color_settings():
    os.system("python color-settings.py")

    """
    config.read(config_file)
    color_settings = config["color_settings"]

    BACKGROUND_COLOR = color_settings["bg_color"]
    BUTTON_BG = color_settings["button_color"]
    BUTTON_HOVER = color_settings["button_color_hover"]

    root.configure(bg=BACKGROUND_COLOR)
    """


# --- INIT --- #
with open(BASE_PATH+"/paths.csv", "r", encoding="utf-8-sig") as csv_file:
    list = csv.reader(csv_file, delimiter=',', quotechar='|')
    for row in list:
        paths = row

for path in paths:
    with open(path + "/songs.csv", "r", encoding="utf-8-sig") as csv_file:
        list = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in list:
            for theme in row[1].split(";"):
                if not theme == "":
                    if theme in themes:
                        themes[theme] += [path + row[0]]
                    else:
                        themes[theme] = [path + row[0]]
pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)

root = Tk()
root.title("RPG Music Tool")
root.geometry("800x600")

root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)

root.config(bg=BACKGROUND_COLOR)

menu = Menu(root)
root.config(menu=menu)

config_menu = Menu(menu)
menu.add_cascade(label="Settings", menu=config_menu)
config_menu.add_command(label="Color Settings", command=open_color_settings)

# LabelFrames
buttons = LabelFrame(root, text="", bg=BACKGROUND_COLOR)
buttons.grid(row=1, column=0)
lower_frame = LabelFrame(root, text="", pady=5, padx=15, bg=BACKGROUND_COLOR, borderwidth=0)
lower_frame.grid(row=3, column=0)
status = LabelFrame(lower_frame, text="", pady=15, padx=15, bg=BACKGROUND_COLOR)
status.grid(row=0, column=0, padx=5)
volume_frame = LabelFrame(lower_frame, text="", pady=15, padx=15, bg=BACKGROUND_COLOR)
volume_frame.grid(row=0,column=1, padx=5)

#Labels
label_current_song = Label(root, text="No Song Playing",font = ("Helvetica",20), bg=BACKGROUND_COLOR)
label_current_song.grid(row=2, column=0, pady=5)

label_current_theme = Label(root, text="No Theme Selected",font = ("Helvetica",20), bg=BACKGROUND_COLOR)
label_current_theme.grid(row=0, column=0, pady=5)

label_duration_song = Label(status, text="00:00 / 00:00", bg=BACKGROUND_COLOR)
label_duration_song.grid(row=0, column=4, padx=5)

song_progress = ttk.Progressbar(status, orient=HORIZONTAL, length=300, mode='determinate')
song_progress.grid(row=0, column=3, padx=5)

label_volume = Label(volume_frame, text="3",font = ("Helvetica",10), bg=BACKGROUND_COLOR)
label_volume.grid(row=1, column=0)

# Images
stop_image = PhotoImage(file="img/stop_img.png")
skip_image = PhotoImage(file="img/skip_img.png")
pause_image = PhotoImage(file="img/pause_img.png")
play_image = PhotoImage(file="img/play_img.png")

# Inputs
button_stop = Button(status, text="", command=stop, image=stop_image, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG)
button_stop.grid(row=0, column=0)

button_pause = Button(status, text="", command=pause, image=pause_image, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG)
button_pause.grid(row=0, column=1)

button_skip = Button(status, text="", command=skip, image=skip_image, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG)
button_skip.grid(row=0, column=2)

volume_changer = ttk.Scale(volume_frame, from_=100, to=0, orient=VERTICAL, value=3, command=volume, length=120)
volume_changer.grid(row=0,column=0)

i = 0
for theme in themes:
    text = theme + "\n" + str(len(themes[theme]))
    theme_play_button = Button(buttons, text=text, command=lambda theme=theme: change_theme(theme), compound=CENTER, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, height=5, width=10)
    theme_play_button.grid(row=i//6+1, column=i % 6)
    i += 1


# --- TK Mainloop --- #
root.mainloop()
