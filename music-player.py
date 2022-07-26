#!/bin/python

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
import sys


# --- CONSTANTS --- #
BASE_PATH = os.path.dirname(__file__)

# --- Variables --- #
global theme
global length
global stopped
global volume

themes = {}
paths = []
first = True
paused = False
stopped = True

tkinter_labels = []
sec_tkinter_labels = []
tkinter_buttons = []
theme_buttons = []


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


def change_volume(pos):
    global volume
    volume = float(pos)
    pygame.mixer.music.set_volume(volume / 100)
    label_volume.config(text=str(int(volume)))


def volume_up():
    global volume
    volume += 1
    pygame.mixer.music.set_volume(volume / 100)
    label_volume.config(text=str(int(volume)))
    volume_changer.config(value=volume)


def volume_down():
    global volume
    volume -= 1
    pygame.mixer.music.set_volume(volume / 100)
    label_volume.config(text=str(int(volume)))
    volume_changer.config(value=volume)


def open_color_settings():
    os.system("python3 color-settings.py")
    update_elements()


def get_settings():
    global BACKGROUND_COLOR
    global BUTTON_BG
    global BUTTON_HOVER
    global TEXT_COLOR
    global SEC_BG_COLOR

    try:
        with open("config.ini") as file:
            pass

    except:
        settings = open("config.ini", 'a')
        settings.write("[color_settings]\nbg_color = #91a3c4\nsec_bg_color = #9baecb\nbutton_color = #7b8cb3\nbutton_color_hover = #868890\ntext_color = #323232")
        settings.close()

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
    SEC_BG_COLOR = color_settings["sec_bg_color"]


def get_paths():
    global paths
    paths = []

    try:
        with open(BASE_PATH+"/paths.csv", "r", encoding="utf-8-sig") as csv_file:
            list = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in list:
                paths = row

    except:
        paths = open("paths.csv", 'a')
        paths.close()

        with open(BASE_PATH+"/paths.csv", "r", encoding="utf-8-sig") as csv_file:
            list = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in list:
                paths = row


def get_themes():
    global themes
    themes = {}

    try:
        for path in paths:
            with open(path + "/songs.csv", "r", encoding="utf-8-sig") as csv_file:
                list = csv.reader(csv_file, delimiter='\\', quotechar='|')
                for row in list:
                    if not len(row) < 2:
                        for theme in row[1].split(";"):
                            if not theme == "":
                                if theme in themes:
                                    themes[theme] += [path + row[0]]
                                else:
                                    themes[theme] = [path + row[0]]
    except:
        pass


def update_elements():
    get_settings()

    root.config(bg=BACKGROUND_COLOR)
    menu.config(bg=SEC_BG_COLOR, activebackground=BUTTON_HOVER)
    config_menu.config(bg=BACKGROUND_COLOR, activebackground=BUTTON_HOVER)

    for element in tkinter_labels:
        element.configure(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)

    for element in sec_tkinter_labels:
        element.configure(bg=SEC_BG_COLOR, fg=TEXT_COLOR)

    for button in tkinter_buttons:
        button.configure(bg=BUTTON_BG, activebackground=BUTTON_HOVER, fg=TEXT_COLOR)

    for button in theme_buttons:
        button.configure(bg=BUTTON_BG, activebackground=BUTTON_HOVER, fg=TEXT_COLOR)


def create_theme_buttons():
    global theme_buttons

    get_paths()
    get_themes()

    i = 0
    for theme in themes:
        text = theme + "\n" + str(len(themes[theme]))
        theme_play_button = Button(buttons, text=text, command=lambda theme=theme: change_theme(theme), compound=CENTER, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, fg=TEXT_COLOR, height=5, width=10)
        theme_play_button.grid(row=i//6+1, column=i % 6)
        i += 1

        theme_buttons += [theme_play_button]


def open_song_settings():
    os.system("python3 song-settings.py")
    for button in theme_buttons:
        button.destroy()

    create_theme_buttons()


def open_path_settings():
    os.system("python3 path-settings.py")
    for button in theme_buttons:
        button.destroy()

    create_theme_buttons()


# --- INIT --- #
pygame.mixer.init()
volume = 5
pygame.mixer.music.set_volume(volume / 100)

get_settings()
get_themes()
get_paths()

root = Tk()
root.title("RPG Music Tool v03")
root.geometry("800x600")

root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)

root.config(bg=BACKGROUND_COLOR)

menu = Menu(root, bg=SEC_BG_COLOR, activebackground=BUTTON_HOVER)
root.config(menu=menu)

config_menu = Menu(menu, bg=BACKGROUND_COLOR, activebackground=BUTTON_HOVER)
menu.add_cascade(label="Settings", menu=config_menu)
config_menu.add_command(label="Color Settings", command=open_color_settings)
config_menu.add_command(label="Path Settings", command=open_path_settings)
config_menu.add_command(label="Song Settings", command=open_song_settings)


# LabelFrames
buttons = LabelFrame(root, text="", bg=BACKGROUND_COLOR)
buttons.grid(row=1, column=0)

lower_frame = LabelFrame(root, text="", pady=5, padx=15, bg=BACKGROUND_COLOR, borderwidth=0)
lower_frame.grid(row=3, column=0)

status = LabelFrame(lower_frame, text="", pady=15, padx=15, bg=SEC_BG_COLOR)
status.grid(row=0, column=0, padx=5)

volume_frame = LabelFrame(lower_frame, text="", pady=15, padx=15, bg=SEC_BG_COLOR)
volume_frame.grid(row=0, column=1, padx=5)

volume_plus_minus_frame = LabelFrame(lower_frame, text="", pady=2, padx=2, bg=SEC_BG_COLOR)
volume_plus_minus_frame.grid(row=0, column=2, padx=5)

tkinter_labels += [buttons, lower_frame]
sec_tkinter_labels += [status, volume_frame, volume_plus_minus_frame]

# Labels
label_current_song = Label(root, text="No Song Playing",font = ("Helvetica",20), bg=BACKGROUND_COLOR)
label_current_song.grid(row=2, column=0, pady=5)

label_current_theme = Label(root, text="No Theme Selected", font = ("Helvetica",20), bg=BACKGROUND_COLOR)
label_current_theme.grid(row=0, column=0, pady=5)

label_duration_song = Label(status, text="00:00 / 00:00", bg=BACKGROUND_COLOR)
label_duration_song.grid(row=0, column=4, padx=5)

song_progress = ttk.Progressbar(status, orient=HORIZONTAL, length=300, mode='determinate')
song_progress.grid(row=0, column=3, padx=5)

label_volume = Label(volume_frame, text=str(volume),font = ("Helvetica",10), bg=BACKGROUND_COLOR)
label_volume.grid(row=1, column=0)

tkinter_labels += [label_current_song, label_current_theme, label_duration_song, label_volume]

# Images
stop_image = PhotoImage(file="img/stop_img.png")
skip_image = PhotoImage(file="img/skip_img.png")
pause_image = PhotoImage(file="img/pause_img.png")
play_image = PhotoImage(file="img/play_img.png")
plus_image = PhotoImage(file="img/plus_img.png")
minus_image = PhotoImage(file="img/minus_img.png")

# Inputs
button_stop = Button(status, command=stop, image=stop_image, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG)
button_stop.grid(row=0, column=0)

button_pause = Button(status, command=pause, image=pause_image, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG)
button_pause.grid(row=0, column=1)

button_skip = Button(status, command=skip, image=skip_image, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG)
button_skip.grid(row=0, column=2)

volume_changer = ttk.Scale(volume_frame, from_=100, to=0, orient=VERTICAL, value=volume, command=change_volume, length=120)
volume_changer.grid(row=0, column=0)

volume_up_button = Button(volume_plus_minus_frame, command=volume_up, image=plus_image, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG)
volume_up_button.grid(row=0, column=1, pady=5)
volume_down_button = Button(volume_plus_minus_frame, command=volume_down, image=minus_image, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG)
volume_down_button.grid(row=1, column=1, pady=5)

tkinter_buttons += [button_stop, button_pause, button_skip, volume_up_button, volume_down_button]

create_theme_buttons()

# --- TK Mainloop --- #
root.mainloop()
