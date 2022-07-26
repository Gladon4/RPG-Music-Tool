# --- IMPORT --- #
from ast import Delete
import os
import time
import random
from tkinter import ttk
from tkinter import *
import csv
from configparser import ConfigParser
import sys
import pygame

# --- CONSTANTS --- #
BASE_PATH = os.path.dirname(__file__)

# --- Variables --- #
themes = {}
inverse_themes = {}
paths = []
songs = {}
text_boxes = []
path_buttons = {}

play_buttons = []
current_song = []

path_label_frame = None
button_update = None

x = 1

# --- Config --- #
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)


# -- Functions --- #
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


def get_themes_and_songs():
    global themes
    global inverse_themes
    global songs
    themes = {}
    inverse_themes = {}
    songs = {}

    try:
        for path in paths:
            songs[path] = []
            with open(path + "/songs.csv", "r", encoding="utf-8-sig") as csv_file:
                list = csv.reader(csv_file, delimiter='\\', quotechar='|')
                for row in list:
                    if not row[0] == '':
                        songs[path] += [row[0]]
                        inverse_themes[row[0]] = []

                    if not len(row) < 2:
                        for theme in row[1].split(";"):
                            if not theme == "":
                                inverse_themes[row[0]] += [theme]
                                if theme in themes:
                                    themes[theme] += [path + row[0]]
                                else:
                                    themes[theme] = [path + row[0]]
    except:
        pass


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


def update_song_list():
    for path in paths:
        songs_in_path = []
        for x in os.listdir(path):
            if x.endswith(".mp3"):
                songs_in_path += [x]

        songs_in_path = sorted(songs_in_path)

        if not songs[path] == songs_in_path:
            rows = []
            for song in songs_in_path:
                row = []
                row += [song]
                if song in inverse_themes:
                    themes_of_song = ""
                    for theme in inverse_themes[song]:
                        themes_of_song += theme + ";"
                    row += [themes_of_song]

                else:
                    row += []
                rows += [row]
            with open(path + "songs.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter='\\')
                csvwriter.writerows(rows)


def update_themes():
    global inverse_themes

    new_inverse_themes = {}

    for path in text_boxes:
        rows = []
        for i, box in enumerate(text_boxes[path]):
            song = songs[path][i]
            themes = box.get(1.0, 'end')[:len(box.get(1.0, 'end')) - 2]

            row = [song, themes]
            new_inverse_themes[song] = themes
            rows += [row]

        with open(path + "songs.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='\\')
            csvwriter.writerows(rows)

    inverse_themes = new_inverse_themes


def play_song(path, song):
    global current_song

    if current_song != [path, song]:
        song_path = path + songs[path][song]

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0)

        if current_song != []:
            play_buttons[current_song[0]][current_song[1]].config(image=play_image)
        play_buttons[song].config(image=stop_image)

        current_song = [path, song]

    else:
        pygame.mixer.music.stop()
        current_song = []
        play_buttons[song].config(image=play_image)


def display_song_list(path):
    global x    
    global play_buttons
    global text_boxes
    global path_label_frame
    global button_update

    if path_label_frame != None:
        button_update.destroy()
        path_label_frame.destroy()

    path_label_frame = LabelFrame(second_frame, font=("Helvetica", 15), bg=BACKGROUND_COLOR, borderwidth=1, fg=TEXT_COLOR, pady=15, padx=15)
    path_label_frame.pack(expand=1, fill=X)

    play_buttons = []
    text_boxes = []

    color = BACKGROUND_COLOR

    for i, song in enumerate(songs[path]):
        button_play = Button(path_label_frame, command=lambda in_=(path, i): play_song(*in_), image=play_image, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, width=25, height=25)
        button_play.grid(row=i, column=0)
        play_buttons += [button_play]

        color = BACKGROUND_COLOR if i % 2 == 0 else SEC_BG_COLOR

        song_label = Label(path_label_frame, text=song, font=("Helvetica", 10), bg=color, fg=TEXT_COLOR, width=55, height=2, borderwidth=0)
        song_label.grid(row=i, column=1)

        themes_text_box = Text(path_label_frame, height=2, width=40, bg=color, fg=TEXT_COLOR, borderwidth=0)
        themes_text_box.grid(row=i, column=2)
        text_boxes += [themes_text_box]
        for theme in inverse_themes[song]:
            themes_text_box.insert('end', theme + ";")

    button_update = Button(second_frame, command=update_themes, text="Update Themes", font=("Helvetica", 12), activebackground=BUTTON_HOVER, bg=BUTTON_BG, width=12, height=3)
    button_update.pack(pady=15)
    
    
    height =  song_set.winfo_height() + x
    song_set.geometry("800x" + str(height))
    x *= -1
    

def display_paths():
    global path_buttons
    
    frame = LabelFrame(second_frame, bg=BACKGROUND_COLOR, pady=15, padx=15)
    frame.pack(expand=1, fill=X)
    
    for j, path in enumerate(paths):
        if BASE_PATH[1] == ":":  # Windows
            directory = path.split("\\")[len(path.split("\\")) - 2]

        else:  # Linux
            directory = path.split("/")[len(path.split("/")) - 2]
        
        path_button = Button(frame, text=directory, command=lambda path=path: display_song_list(path), compound=CENTER, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, fg=TEXT_COLOR, height=3, width=12)
        path_button.grid(row=j//6+1, column=j % 6)
        path_buttons[path] = path_button
    




# --- INIT --- #
get_paths()
get_themes_and_songs()
get_settings()
update_song_list()

pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)

song_set = Tk()
song_set.title("Song Settings")
song_set.geometry("800x800")
song_set.configure(bg=BACKGROUND_COLOR)

main_frame = Frame(song_set, bg=BACKGROUND_COLOR)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set, bg=BACKGROUND_COLOR)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

second_frame = Frame(my_canvas, bg=BACKGROUND_COLOR)
my_canvas.create_window((0,0), window=second_frame, anchor="n")

top_label = Label(second_frame, text="Change Song Themes", font=("Helvetica", 20), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
top_label.pack(fill=X)

play_image = PhotoImage(file="img/play_img.png").subsample(3, 3)
stop_image = PhotoImage(file="img/stop_img.png").subsample(3, 3)

display_paths()

song_set.mainloop()
