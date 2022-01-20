import csv
from tkinter import *
from tkinter import ttk
import pygame
import random

moods = {}
# paths = ["CK3/", "Pillars_of_Eternity/"]
with open("paths.csv", "r", encoding="utf-8-sig") as csv_file:
    list = csv.reader(csv_file, delimiter=',', quotechar='|')
    for row in list:
        paths = row

current_mood = NONE
song = NONE
song_path = ""
song_timer = 0
time_left = 0
paused = False

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()


def update():
    global time_left
    global song_timer
    global paused
    global current_mood

    if not song == NONE:
        song_progress['value'] = int(
            (song_timer - time_left) / song_timer * 100)
        pygame.mixer.Sound.set_volume(song, volume.get() / 100)

    if not paused and not song == NONE:
        time_left -= 10
        if time_left <= 3000:
            get_next_song(current_mood)

    if time_left > 3000:
        label_current_song.after(10, update)


def get_next_song(mood):
    global song
    global song_path
    global current_mood
    if not song == NONE:
        pygame.mixer.Sound.stop(song)
        song_id = random.randint(0, len(moods[mood]) - 1)
        current_mood = mood
        song_path = moods[mood][song_id]
        label_current_song.after(2200, play)

    else:
        song_id = random.randint(0, len(moods[mood]) - 1)
        current_mood = mood
        song_path = moods[mood][song_id]
        play()


def play():
    global song
    global song_path
    global time_left
    global song_timer

    song = pygame.mixer.Sound(song_path)
    pygame.mixer.Sound.play(song)
    label_current_song.config(text=song_path)

    song_timer = pygame.mixer.Sound.get_length(song) * 1000
    time_left = song_timer
    update()


def pause():
    global paused

    paused = True
    pygame.mixer.pause()


def unpause():
    global paused

    paused = False
    pygame.mixer.unpause()


for path in paths:
    with open(path + "/songs.csv", "r", encoding="utf-8-sig") as csv_file:
        list = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in list:
            moods_of_song = row[1].split(";")
            for mood in moods_of_song:
                if not mood == "":
                    if mood in moods:
                        moods[mood] += [path + row[0]]
                    else:
                        moods[mood] = [path + row[0]]

print(moods)

root = Tk()
root.title("RPG Mood Song Player")
root.geometry("800x600")

root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)


buttons = LabelFrame(root, text="", pady=15, padx=25)
buttons.grid(row=1, column=0)
status = LabelFrame(root, text="", pady=15, padx=15)
status.grid(row=3, column=0)

i = 0
for mood in moods:
    mood_play_button = Button(
        buttons, text=mood, command=lambda mood=mood: get_next_song(mood), height=5, width=10)
    mood_play_button.grid(row=i//6+1, column=i % 6)
    i += 1


label_current_song = Label(root, text="")
label_current_song.grid(row=0, column=0)

song_progress = ttk.Progressbar(
    status, orient=HORIZONTAL, length=400, mode='determinate')
song_progress.grid(row=0, column=2)

volume = Scale(status, from_=100, to=0, length=120, width=25)
volume.set(10)
volume.grid(row=0, column=3)


button_pause = Button(status, text="Pause", command=pause)
button_pause.grid(row=0, column=1)

button_unpause = Button(status, text="Play", command=unpause)
button_unpause.grid(row=0, column=0)

col_count, row_count = root.grid_size()

for col in range(col_count):
    root.grid_columnconfigure(col, minsize=100)

for row in range(row_count):
    root.grid_rowconfigure(row, minsize=100)

root.mainloop()
