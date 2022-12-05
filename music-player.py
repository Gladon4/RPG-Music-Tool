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
from appdirs import *
from tkinter.colorchooser import askcolor


# --- CONSTANTS --- #

# --- Variables --- #
theme = None
length = None
stopped = None
volume = None

themes = {}
paths = []
first = True
paused = False
stopped = True

current_tab = 0

tkinter_labels = []
sec_tkinter_labels = []
tkinter_buttons = []
theme_buttons = {}

themes = {}
inverse_themes = {}
paths = []
songs = {}
sfx_paths = []
sfxs = {}
text_box_song_paths_list = []
path_buttons = {}
current_path = ""

play_buttons = []
current_song = []

path_label_frame = None
button_update = None

song_setting_objects = []

# --- Functions --- #
def change_theme(next_theme):
    global theme
    global stopped
    global paused
    global theme_buttons

    stopped = False
    paused = False
    
    if theme != None:
        theme_buttons[theme].config(bg=BUTTON_BG, relief=RAISED)
    
    theme_buttons[next_theme].config(bg=BUTTON_HOVER, relief=SUNKEN)
    
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

    if sys.platform.startswith('win32'): # Windows
        path = song.split("\\")[len(song.split("\\")) - 2]
        song_name = song.split("\\")[len(song.split("\\")) - 1].split(".mp3")[0]

    elif sys.platform.startswith('linux'): # Linux
        path = song.split("/")[len(song.split("/")) - 2]
        song_name = song.split("/")[len(song.split("/")) - 1].split(".mp3")[0]
    
    label_current_song.config(text=song_name)
    label_current_song_path.config(text=path)

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
    global theme_buttons
    global theme

    stopped = True
    pygame.mixer.music.stop()
    
    if theme != None:
        theme_buttons[theme].config(relief=RAISED, bg=BUTTON_BG)

    label_current_song.config(text="No Song Playing")
    label_current_song_path.config(text="No Song Playing")
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
    volume_changer.config(value=volume)
    save()


def volume_up():
    change_volume(volume+1)


def volume_down():
    change_volume(volume-1)


def create_config_path():
    path = user_config_dir("rpg-mt", "Gladon")

    if sys.platform.startswith('linux'):
        try:
            os.mkdir(path)
        except:
            pass
        
    elif sys.platform.startswith('win32'):
        try:
            path2 = "\\".join(path.split("\\")[:-1])
            os.mkdir(path2)
            os.mkdir(path)
        except:
            pass
            
            
def get_settings():
    global BACKGROUND_COLOR
    global BUTTON_BG
    global BUTTON_HOVER
    global TEXT_COLOR
    global SEC_BG_COLOR

    global UI_SCALE
    global ROW_LENGTH
    global volume
    global SFX_ON_THEMES

    path = user_config_dir("rpg-mt", "Gladon")

    try:
        with open(path + "/config.ini") as file:
            pass

        # --- Config --- #
        config_file = path + "/config.ini"
        config = ConfigParser()
        config.read(config_file)

        # Color
        color_settings = config["color_settings"]

        BACKGROUND_COLOR = color_settings["bg_color"]
        BUTTON_BG = color_settings["button_color"]
        BUTTON_HOVER = color_settings["button_color_hover"]
        TEXT_COLOR = color_settings["text_color"]
        SEC_BG_COLOR = color_settings["sec_bg_color"]

        # App Settings
        app_settings = config["app_settings"]
        UI_SCALE = int(app_settings["ui_scale"])
        ROW_LENGTH = int(app_settings["row_length"])
        volume = int(float(app_settings["volume"]))
        SFX_ON_THEMES = int(app_settings["sfx_on_themes"])

    except:
        write_default_settings()
        get_settings()    



def get_paths():
    global paths
    global sfx_paths
    paths = []
    sfx_paths = []
    
    path = user_config_dir("rpg-mt", "Gladon")

    # Songs
    try:
        with open(path + "/paths.csv", "r", encoding="utf-8-sig") as csv_file:
            list = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in list:
                if row != []:
                    paths = row

    except:
        paths = open(path + "/paths.csv", 'a')
        paths.close()

        with open(path + "/paths.csv", "r", encoding="utf-8-sig") as csv_file:
            list = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in list:
                paths = row


    # SFX
    try:
        with open(path + "/sfx-paths.csv", "r", encoding="utf-8-sig") as csv_file:
            list = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in list:
                if row != []:
                    sfx_paths = row

    except:
        sfx_paths = open(path + "/sfx-paths.csv", 'a')
        sfx_paths.close()

        with open(path + "/sfx-paths.csv", "r", encoding="utf-8-sig") as csv_file:
            list = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in list:
                sfx_paths = row


def get_themes():
    global themes
    global inverse_themes
    global songs
    global paths
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
    

def get_sfx():
    global sfxs
    global sfx_paths

    sfxs = {}

    try:
        for path in sfx_paths:
            sfxs[path] = []
            with open(path + "/sfx.csv", "r", encoding="utf-8-sig") as csv_file:
                list = csv.reader(csv_file, delimiter='\\', quotechar='|')
                for row in list:
                    if not row[0] == '':
                        sfxs[path] += [row[0]]
    except:
        pass
    

def update_elements():
    global tkinter_labels
    global sec_tkinter_labels
    global tkinter_buttons
    global theme_buttons
    
    get_settings()

    theme_frame.config(bg=BACKGROUND_COLOR)
    song_settings_frame.config(bg=BACKGROUND_COLOR)
    path_settings_frame.config(bg=BACKGROUND_COLOR)
    settings_frame.config(bg=BACKGROUND_COLOR)

    for element in tkinter_labels:
        element.configure(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)

    for element in sec_tkinter_labels:
        element.configure(bg=SEC_BG_COLOR, fg=TEXT_COLOR)

    for button in tkinter_buttons:
        button.configure(bg=BUTTON_BG, activebackground=BUTTON_HOVER, fg=TEXT_COLOR)

    for theme in theme_buttons:
        theme_buttons[theme].configure(bg=BUTTON_BG, activebackground=BUTTON_HOVER, fg=TEXT_COLOR)


def create_theme_buttons():
    global theme_buttons
    global theme

    get_themes()
    
    theme_buttons = {}

    i = 0
    for _theme in themes:
        text = _theme
        theme_play_button = Button(theme_buttons_frame, text=text, command=lambda _theme=_theme: change_theme(_theme), compound=CENTER, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, fg=TEXT_COLOR, height=int(2.5*UI_SCALE), width=int(5*UI_SCALE))
        theme_play_button.grid(row=i//ROW_LENGTH+1, column=i % ROW_LENGTH)
        
        if theme == _theme:
            theme_play_button.config(bg=BUTTON_HOVER, relief=SUNKEN)
        
        i += 1

        theme_buttons[_theme] = theme_play_button


def create_sfx_buttons():
    global sfx_buttons

    temp_sfx_list = []

    for path in sfxs:
        for sfx in sfxs[path]:
            temp_sfx_list += [path + sfx]


    sfx_buttons = {}

    i = 0
    for sfx in temp_sfx_list:
        if sys.platform.startswith('win32'):
            text = sfx.split("\\")
            text = text[-1].split(".mp3")[0]

        elif sys.platform.startswith('linux'):
            text = sfx.split("/")
            text = text[-1].split(".mp3")[0]

        theme_play_button = Button(sfx_buttons_frame, text=text, command=lambda sfx=sfx: play_sfx(sfx), compound=CENTER, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, fg=TEXT_COLOR, height=int(2.5*UI_SCALE), width=int(5*UI_SCALE))
        theme_play_button.grid(row=i//ROW_LENGTH+1, column=i % ROW_LENGTH)
        
        i += 1

        sfx_buttons[sfx] = theme_play_button

    

def play_sfx(sfx_path):
    sfx = pygame.mixer.Sound(sfx_path)
    pygame.mixer.Sound.set_volume(sfx, 4 * (volume / 100))
    pygame.mixer.Sound.play(sfx)


def create_theme_frame():
    global tkinter_labels
    global sec_tkinter_labels
    global tkinter_buttons
    global buttons
    global label_current_theme
    global button_pause
    global label_current_song
    global label_duration_song
    global song_progress
    global label_volume
    global volume_changer
    global label_current_song_path
    global theme_buttons_frame
    global sfx_buttons_frame

    # LabelFrames
    
    theme_buttons_frame = LabelFrame(theme_frame, text="", bg=BACKGROUND_COLOR, padx=25, borderwidth=0, pady=10)
    theme_buttons_frame.grid(row=1, column=0)

    sfx_buttons_frame = LabelFrame(theme_frame, text="", bg=BACKGROUND_COLOR, padx=25, borderwidth=0, pady=10)
    sfx_buttons_frame.grid(row=5, column=0)
    
    lower_frame = LabelFrame(theme_frame, text="", pady=5, padx=15, bg=BACKGROUND_COLOR, borderwidth=0)
    lower_frame.grid(row=4, column=0)

    status = LabelFrame(lower_frame, text="", pady=15, padx=15, bg=SEC_BG_COLOR, borderwidth=1)
    status.grid(row=0, column=0, padx=5)

    volume_frame = LabelFrame(lower_frame, text="", pady=15, padx=15, bg=SEC_BG_COLOR,)
    volume_frame.grid(row=0, column=1, padx=5)

    volume_plus_minus_frame = LabelFrame(lower_frame, text="", pady=2, padx=2, bg=BACKGROUND_COLOR, borderwidth=0)
    volume_plus_minus_frame.grid(row=0, column=2, padx=5)

    tkinter_labels += [lower_frame, theme_buttons_frame, volume_plus_minus_frame]
    sec_tkinter_labels += [status, volume_frame]

    # Labels
    label_current_song = Label(theme_frame, text="No Song Playing",font = ("Helvetica",20), bg=BACKGROUND_COLOR)
    label_current_song.grid(row=2, column=0)
    
    label_current_song_path = Label(theme_frame, text="No Song Playing",font = ("Helvetica",12), bg=BACKGROUND_COLOR)
    label_current_song_path.grid(row=3, column=0)

    label_current_theme = Label(theme_frame, text="No Theme Selected", font = ("Helvetica",20), bg=BACKGROUND_COLOR)
    label_current_theme.grid(row=0, column=0, pady=5)

    label_duration_song = Label(status, text="00:00 / 00:00", bg=BACKGROUND_COLOR)
    label_duration_song.grid(row=0, column=4, padx=5)

    song_progress = ttk.Progressbar(status, orient=HORIZONTAL, length=300, mode='determinate')
    song_progress.grid(row=0, column=3, padx=5)

    label_volume = Label(volume_frame, text=str(volume),font = ("Helvetica",10), bg=BACKGROUND_COLOR)
    label_volume.grid(row=1, column=0)

    tkinter_labels += [label_current_song, label_current_theme, label_duration_song, label_volume]

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

    if SFX_ON_THEMES: create_sfx_buttons()


def create_path_settings_frame():
    global text_box_song_paths
    global text_box_sfx_paths
    global tkinter_labels
    global tkinter_buttons
    
    paths_text = ""
    for p in paths:
        paths_text += p + "\n"

    song_path_label_title = Label(path_settings_frame, text="Configure Song Paths",font=("Helvetica",20), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    song_path_label_title.pack(pady=10)

    text_box_song_paths = Text(path_settings_frame, height=20, width=90, bg=BACKGROUND_COLOR, fg=TEXT_COLOR,borderwidth=0)
    text_box_song_paths.pack()
    text_box_song_paths.insert('end', paths_text)
    text_box_song_paths.config(state='normal')
    text_box_song_paths.tag_configure("warning", foreground="red")
    
    paths_text = ""
    for p in sfx_paths:
        paths_text += p + "\n"

    sfx_path_label_title = Label(path_settings_frame, text="Configure Sound Effect Paths",font=("Helvetica",20), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    sfx_path_label_title.pack(pady=10)

    text_box_sfx_paths = Text(path_settings_frame, height=10, width=90, bg=BACKGROUND_COLOR, fg=TEXT_COLOR,borderwidth=0)
    text_box_sfx_paths.pack()
    text_box_sfx_paths.insert('end', paths_text)
    text_box_sfx_paths.config(state='normal')
    text_box_sfx_paths.tag_configure("warning", foreground="red")

    save_paths_button = Button(path_settings_frame, command=update_paths, text="Save Paths", borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, pady=10)
    save_paths_button.pack(pady=10)

    tkinter_labels += [song_path_label_title, sfx_path_label_title, text_box_song_paths, text_box_sfx_paths]
    tkinter_buttons += [save_paths_button]


def update_paths():
    save_paths()
    get_paths()


def save_paths():
    new_song_paths = text_box_song_paths.get(1.0, 'end').split()
    new_sfx_paths = text_box_sfx_paths.get(1.0, 'end').split()
    text_box_song_paths.delete(1.0, 'end')
    text_box_sfx_paths.delete(1.0, 'end')

    set_path = user_config_dir("rpg-mt", "Gladon")

    # Songs
    new_text = []

    for path in new_song_paths:
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
            text_box_song_paths.insert('end', i[0] + "\n", None)
        else:
            text_box_song_paths.insert('end', i[0] + "\n", "warning")

    with open(set_path + "/paths.csv", "w") as csv_file:
        write = csv.writer(csv_file)
        write.writerow(new_song_paths)


    # SFX
    new_text = []

    for path in new_sfx_paths:
        try:
            with open(path + "/sfx.csv") as file:
                new_text += [(path, True)]

        except:
            try:
                sfx = open(path + "/sfx.csv", 'a')
                sfx.close()
                new_text += [(path, True)]

            except:
                new_text += [(path, False)]

    for i in new_text:
        if i[1]:
            text_box_sfx_paths.insert('end', i[0] + "\n", None)
        else:
            text_box_sfx_paths.insert('end', i[0] + "\n", "warning")

    with open(set_path + "/sfx-paths.csv", "w") as csv_file:
        write = csv.writer(csv_file)
        write.writerow(new_sfx_paths)


def create_song_settings_frame():
    global second_frame
    global path_label
    global song_setting_objects
    global my_canvas
    
    main_frame = Frame(song_settings_frame, bg=BACKGROUND_COLOR)
    main_frame.pack(fill="both", expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill="both", expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set, bg=BACKGROUND_COLOR)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

    second_frame = Frame(my_canvas, bg=BACKGROUND_COLOR)
    my_canvas.create_window((0,0), window=second_frame, anchor="n")

    top_label = Label(second_frame, text="Change Song Themes", font=("Helvetica", 20), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    top_label.pack(fill=X)

    display_paths()

    path_label = Label(second_frame, text="No Path Selected", font=("Helvetica", 15), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    path_label.pack(fill=X)
    
    song_setting_objects = [main_frame, my_canvas, my_scrollbar, second_frame, top_label, path_label]


def update_themes():
    global inverse_themes
    global current_path

    rows = []
    if current_path != "":
        for i, box in enumerate(text_box_song_paths_list):
            song = songs[current_path][i]
            themes = box.get(1.0, 'end')[:len(box.get(1.0, 'end')) - 2]

            row = [song, themes]
            inverse_themes[song] = [themes] if themes != '' else []
            rows += [row]

        with open(current_path + "songs.csv", 'w', newline="") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='\\')
            csvwriter.writerows(rows)


def update_song_list():
    for path in paths:
        songs_in_path = []
        try:
            for x in os.listdir(path):
                if x.endswith(".mp3"):
                    songs_in_path += [x]

            songs_in_path = sorted(songs_in_path)
        except:
            songs_in_path = []

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

            with open(path + "songs.csv", 'w', newline="") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter='\\')
                csvwriter.writerows(rows)

    for path in sfx_paths:
        sfx_in_path = []
        try:
            for x in os.listdir(path):
                if x.endswith(".mp3"):
                    sfx_in_path += [x]

            sfx_in_path = sorted(sfx_in_path)
        except:
            sfx_in_path = []

        if not sfxs[path] == sfx_in_path:
            rows = []
            for sfx in sfx_in_path:
                row = []
                row += [sfx]
                rows += [row]

            with open(path + "sfx.csv", 'w', newline="") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter='\\')
                csvwriter.writerows(rows)


def play_song(path, song):
    global current_song

    if current_song != [path, song]:
        song_path = path + songs[path][song]

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0)

        if current_song != []:
            play_buttons[current_song[1]].config(image=play_image_small)
        play_buttons[song].config(image=stop_image_small)

        current_song = [path, song]

    else:
        pygame.mixer.music.stop()
        current_song = []
        play_buttons[song].config(image=play_image_small)
   

def display_song_list(path):
    global current_path
    global x    
    global play_buttons
    global path_label_frame
    global button_update
    global text_box_song_paths_list
    global path_label
    global inverse_themes
    
    if current_song != []:
        play_song(*current_song)
    
    update_song_list()
    
    if current_path != "":
        update_themes()
    
    current_path = path

    if path_label_frame != None:
        path_label_frame.destroy()
        
    if button_update != None:
        button_update.destroy()
        
    if sys.platform.startswith('win32'):  # Windows
        directory = path.split("\\")[len(path.split("\\")) - 2]

    elif sys.platform.startswith('linux'):  # Linux
        directory = path.split("/")[len(path.split("/")) - 2]
    

    path_label.configure(text=directory)

    path_label_frame = LabelFrame(second_frame, font=("Helvetica", 15), bg=BACKGROUND_COLOR, borderwidth=1, fg=TEXT_COLOR, pady=15, padx=15)
    path_label_frame.after(200, lambda : adjust_scrollregion())
    path_label_frame.pack(expand=1, fill=X)

    play_buttons = []
    text_box_song_paths_list = []

    color = BACKGROUND_COLOR

    for i, song in enumerate(songs[path]):
        button_play = Button(path_label_frame, command=lambda in_=(path, i): play_song(*in_), image=play_image_small, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, width=25, height=25)
        button_play.grid(row=i+1, column=0)
        play_buttons += [button_play]

        color = BACKGROUND_COLOR if i % 2 == 0 else SEC_BG_COLOR

        song_label = Label(path_label_frame, text=song, font=("Helvetica", 10), bg=color, fg=TEXT_COLOR, width=55, height=2, borderwidth=0)
        song_label.grid(row=i+1, column=1)

        themes_text_box_song_paths = Text(path_label_frame, height=2, width=40, bg=color, fg=TEXT_COLOR, borderwidth=0)
        themes_text_box_song_paths.grid(row=i+1, column=2)
        text_box_song_paths_list += [themes_text_box_song_paths]
        
        for theme in inverse_themes[song]:
            themes_text_box_song_paths.insert('end', theme + ";")


def adjust_scrollregion():
    global my_canvas
    my_canvas.configure(scrollregion=my_canvas.bbox("all"))
   
    
def display_paths():
    global path_buttons
    global second_frame
    
    frame = LabelFrame(second_frame, bg=BACKGROUND_COLOR, pady=15, padx=15)
    frame.pack(expand=1, fill=X)
    
    for j, path in enumerate(paths):
        if sys.platform.startswith('win32'):  # Windows
            directory = path.split("\\")[len(path.split("\\")) - 2]

        elif sys.platform.startswith('linux'):  # Linux
            directory = path.split("/")[len(path.split("/")) - 2]
        
        path_button = Button(frame, text=directory, command=lambda path=path: display_song_list(path), compound=CENTER, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, fg=TEXT_COLOR, height=3, width=12)
        path_button.grid(row=j//6+1, column=j % 6)
        path_buttons[path] = path_button


def create_settings_frame():
    global tkinter_labels
    global sec_tkinter_labels

    global ui_scale_label
    global ui_scale_slider
    global row_length_label
    global row_length_slider

    global sfx_on_themes_checkbox

    global colors
    global color_elems
    global colors_frame
    global tkinter_labels
    global tkinter_buttons

    # -- App Settings -- #

    label_title_app_settings = Label(settings_frame, text="Application Settings",font=("Helvetica",20), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    label_title_app_settings.pack()

    ui_setting_frame = LabelFrame(settings_frame, text="UI Settings", font=("Helvetica",15), pady=15, padx=15, bg=SEC_BG_COLOR, borderwidth=0)
    ui_setting_frame.pack(pady=10)

    label_subtitle_ui_scale = Label(ui_setting_frame, text="Theme Button Scale",font=("Helvetica",12), padx=15, bg=SEC_BG_COLOR, fg=TEXT_COLOR)
    label_subtitle_ui_scale.grid(row=0, column=0)

    ui_scale_slider = ttk.Scale(ui_setting_frame, from_=1, to=5, value=UI_SCALE, command=change_ui_scale, length=200)
    ui_scale_slider.grid(row=0, column=1, pady=10)

    ui_scale_label = Label(ui_setting_frame, text=UI_SCALE, font=("Helvetica",12), padx=10, bg=SEC_BG_COLOR, fg=TEXT_COLOR)
    ui_scale_label.grid(row=0, column=2)


    label_subtitle_row_lenght = Label(ui_setting_frame, text="Themes Buttons per Row",font=("Helvetica",12), padx=15, bg=SEC_BG_COLOR, fg=TEXT_COLOR)
    label_subtitle_row_lenght.grid(row=2, column=0)

    row_length_slider = ttk.Scale(ui_setting_frame, from_=3, to=10, value=ROW_LENGTH, command=change_row_length, length=200)
    row_length_slider.grid(row=2, column=1, pady=10)

    row_length_label = Label(ui_setting_frame, text=ROW_LENGTH, font=("Helvetica",12), padx=10, bg=SEC_BG_COLOR, fg=TEXT_COLOR)
    row_length_label.grid(row=2, column=2)


    sfx_on_themes_label = Label(ui_setting_frame, text="Display SFX on Themes Tab", font=("Helvetica",12), padx=10, bg=SEC_BG_COLOR, fg=TEXT_COLOR)
    sfx_on_themes_label.grid(row=3, column=0, pady=10)

    var1 = True

    sfx_on_themes_checkbox = Checkbutton(ui_setting_frame, text="  (Requires Restart)  ", command=change_sfx_on_themes, height=2, bg=BUTTON_BG, activebackground=BUTTON_HOVER)
    sfx_on_themes_checkbox.grid(row=3, column=1)

    if SFX_ON_THEMES: sfx_on_themes_checkbox.select()
    

    tkinter_labels += [label_title_app_settings]
    tkinter_buttons += [sfx_on_themes_checkbox]
    sec_tkinter_labels += [ui_setting_frame, label_subtitle_ui_scale, ui_scale_label, label_subtitle_row_lenght, row_length_label, sfx_on_themes_label]
    
    # -- Color Settings -- #

    bg_color = BACKGROUND_COLOR
    but_col = BUTTON_BG
    but_hov_col = BUTTON_HOVER
    text_color = TEXT_COLOR
    sec_bg_col = SEC_BG_COLOR
    
    colors = {"Background Color":bg_color, "Secondary Background Color": sec_bg_col, "Text Color":text_color, "Primary Button Color":but_col, "Secondary Button Color":but_hov_col}
    color_elems = [] 
    
    label_title_color_settings = Label(settings_frame, text="Color Settings",font=("Helvetica",20), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    label_title_color_settings.pack(pady=15)

    colors_frame = LabelFrame(settings_frame, bg=BACKGROUND_COLOR, borderwidth=0)
    colors_frame.pack()

    i = 0
    for color in colors:
        label_frame = LabelFrame(colors_frame, bg=SEC_BG_COLOR, text=color)
        label_frame.grid(row=i//3+1, column=i % 3, padx=6, pady=6)
        color_label_frame = LabelFrame(label_frame, bg=BACKGROUND_COLOR, borderwidth=3)
        color_label_frame.grid(row=0, column=0)
        color_label = Label(color_label_frame, width=18, height=9, bg=colors[color])
        color_label.pack()
        picker_button = Button(label_frame, text="Pick Color", command=lambda i=i: change_color(i), activebackground=BUTTON_HOVER, bg=BUTTON_BG, height=4, width=6)
        picker_button.grid(row=0, column=1, padx=5)

        color_elems += [[label_frame, color_label_frame, color_label, picker_button, color]]

        i += 1

    tkinter_labels += [label_title_color_settings]

    # -- Reset Settings -- #
    reset_button = Button(settings_frame, text="Reset Settings", command=reset_settings, activebackground=BUTTON_HOVER, bg=BUTTON_BG, height=3, width=12)
    reset_button.pack(pady=15)


def reset_settings():
    global colors

    write_default_settings()
    get_settings()

    ui_scale_slider.config(value=UI_SCALE)
    ui_scale_label.config(text=UI_SCALE)
    row_length_slider.config(value=ROW_LENGTH)
    row_length_label.config(text=ROW_LENGTH)

    bg_color = BACKGROUND_COLOR
    but_col = BUTTON_BG
    but_hov_col = BUTTON_HOVER
    text_color = TEXT_COLOR
    sec_bg_col = SEC_BG_COLOR
    
    colors = {"Background Color":bg_color, "Secondary Background Color": sec_bg_col, "Text Color":text_color, "Primary Button Color":but_col, "Secondary Button Color":but_hov_col}
  
    reload_colors()


def change_ui_scale(pos):
    global UI_SCALE

    UI_SCALE = int(float(pos))
    ui_scale_label.config(text=UI_SCALE)
    ui_scale_slider.config(value=UI_SCALE)


def change_row_length(pos):
    global ROW_LENGTH

    ROW_LENGTH = int(float(pos))
    row_length_label.config(text=ROW_LENGTH)
    row_length_slider.config(value=ROW_LENGTH)


def change_sfx_on_themes():
    global SFX_ON_THEMES

    SFX_ON_THEMES = 0 if SFX_ON_THEMES else 1

    save()
    get_settings()


def save():
    path = user_config_dir("rpg-mt", "Gladon")

    config = ConfigParser()
    config["color_settings"] = {"bg_color" : colors["Background Color"],
                                "sec_bg_color" : colors["Secondary Background Color"],
                                "button_color" : colors["Primary Button Color"],
                                "button_color_hover" : colors["Secondary Button Color"],
                                "text_color" : colors["Text Color"]}

    config["app_settings"] =   {"ui_scale" : UI_SCALE,
                                "row_length": ROW_LENGTH,
                                "volume" : volume,
                                "sfx_on_themes" : SFX_ON_THEMES}


    with open(path + '/config.ini', 'w') as configfile:
        config.write(configfile)


def write_default_settings():
    # --- Defaults --- #
    # Color
    bg_col =      "#91a3c4"
    sec_bg_col =    "#9baecb"
    but_col =       "#7b8cb3"
    sec_but_col =   "#668bb0"
    text_col =      "#323232"

    # App Settings
    ui_scale =      2
    row_length =    6
    def_vol =       15
    def_sfx_pos =   1

    path = user_config_dir("rpg-mt", "Gladon")

    config = ConfigParser()
    config["color_settings"] = {"bg_color" : bg_col,
                                "sec_bg_color" : sec_bg_col,
                                "button_color" : but_col,
                                "button_color_hover" : sec_but_col,
                                "text_color" : text_col}

    config["app_settings"] = {"ui_scale" : ui_scale,
                                "row_length": row_length,
                                "volume" : def_vol,
                                "sfx_on_themes" : def_sfx_pos}

    with open(path + '/config.ini', 'w') as configfile:
        config.write(configfile)


def change_color(index):
    global color_elems
    global colors

    title = "Choose " + color_elems[index][4]

    color = askcolor(colors[color_elems[index][4]], title=title)

    color_elems[index][2].configure(bg=color[1])
    colors[color_elems[index][4]] = color[1]

    reload_colors()
    update_elements()


def reload_colors():
    global colors_frame
    
    settings_frame.configure(bg = colors["Background Color"])
    colors_frame.configure(bg = colors["Background Color"], fg = colors["Text Color"])

    color_index = ["Background Color", "Secondary Background Color", "Text Color", "Primary Button Color","Secondary Button Color"]
    for i in range(len(color_elems)):
        color_elems[i][0].configure(bg = colors["Secondary Background Color"], fg = colors["Text Color"])
        color_elems[i][1].configure(bg = colors["Background Color"], fg = colors["Text Color"])
        color_elems[i][2].configure(bg = colors[color_index[i]])
        color_elems[i][3].configure(bg = colors["Primary Button Color"], activebackground=colors["Secondary Button Color"], fg = colors["Text Color"])


def on_tab_change(e):
    global current_path
    global current_tab
    
    tab = notebook.index(notebook.select())
    update_themes()
    save()
    update_elements()
    
    if current_tab == notebook.index(path_settings_frame):
        update_paths()
    
    
    current_path = ""
    
    if tab == notebook.index(theme_frame):
        for theme in theme_buttons:
            theme_buttons[theme].destroy()
        create_theme_buttons()        
        update_song_list()
        
    if tab == notebook.index(song_settings_frame):
        for o in song_setting_objects:
            o.destroy()
            
        for path in path_buttons:
            path_buttons[path].destroy()
        
        create_song_settings_frame()
        
    current_tab = tab


# --- INIT --- #
pygame.mixer.init(frequency=44100)

create_config_path()
get_settings()
get_paths()
get_themes()
get_sfx()
update_song_list()



pygame.mixer.music.set_volume(volume / 100)

root = Tk()
root.title("RPG Music Tool v05_dev")
root.geometry("800x800")

style = ttk.Style()
# style.layout('TNotebook.Tab', [])

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=1)

theme_frame = Frame(notebook, width=0, height=0, bg=BACKGROUND_COLOR)

path_settings_frame = Frame(notebook, width=800, height=800, bg=BACKGROUND_COLOR)

song_settings_frame = Frame(notebook, width=800, height=800, bg=BACKGROUND_COLOR)

settings_frame = Frame(notebook, width=800, height=800, bg=BACKGROUND_COLOR)

notebook.add(theme_frame, text="Themes")
notebook.add(path_settings_frame, text="Paths")
notebook.add(song_settings_frame, text="Song Themes")
notebook.add(settings_frame, text="Settings")

notebook.enable_traversal() 

notebook.bind('<<NotebookTabChanged>>', on_tab_change)

theme_frame.grid_rowconfigure(0, weight=0)
theme_frame.grid_columnconfigure(0, weight=1)

# Images
if getattr(sys, 'frozen', False):
    stop_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/stop_img.png"))
    skip_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/skip_img.png"))
    pause_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/pause_img.png"))
    play_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/play_img.png"))
    plus_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/plus_img.png"))
    minus_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/minus_img.png"))
    
else:
    stop_image = PhotoImage(file="img/stop_img.png")
    skip_image = PhotoImage(file="img/skip_img.png")
    pause_image = PhotoImage(file="img/pause_img.png")
    play_image = PhotoImage(file="img/play_img.png")
    plus_image = PhotoImage(file="img/plus_img.png")
    minus_image = PhotoImage(file="img/minus_img.png")

play_image_small = play_image.subsample(3, 3)
stop_image_small = stop_image.subsample(3, 3)

create_theme_frame()
create_path_settings_frame()
create_song_settings_frame()
create_settings_frame()

"""
notebook.select(theme_frame)

notebook.hide(settings_frame)

def test():
    notebook.select(settings_frame)

b = Button(theme_frame, text= "test", command=test)
b.grid(row=10, column=0)
"""

# --- TK Mainloop --- #
root.mainloop()
