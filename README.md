# RPG-Music-Tool (ver. 0.2.5 [Settings Update])

A small music tool for TTRPGs.

This Tool allows you to play music based on the current mood or setting for your TableTop RolePlayingGames.
This Program uses local music files, instead of for example a Spotify Playlist. So you can always use it as long as you have your music with you.

## Python Dependencies (Use pip to install):

pygame

tkinter

ttk

mutagen

This is python, so just install python3 and libraries and it should work.

## How to set up:
### 1.

Supports Windows and Linux as of now!

Download the repository, either as a zip and unzip it, or with git clone.

### 2.

In the directory of your songs create a songs.csv, which lists all songs (with file ending) you want to include.
Separate them by line breaks and add the fitting moods after like this:

Combat A.mp3,Combat;Tense\
Combat B.mp3,Combat;War\
Combat C.mp3,Combat\
Tavern A.mp3,Tavern;Festive

### 3.

Create a paths.csv (or rename the example_paths.csv) in the directory of the program, and put in the paths to the music directories, separate with comma (,).

Example for Linux:

/home/[user]/Music/RPG/,/home/[user]/Documents/music/

Example for Windows:

C:\Users\[user]\Music\RPG\,C:\Users\[user]\Documents\music\

That's it.


## How to Use it:

The Programm should display all created moods and how many songs are associated with that mood.
Just click on the mood you currently need and it should start playing a random sequence of songs with the chosen mood.
(This is suited well for touch displays, if you have one)

![image](https://user-images.githubusercontent.com/58821835/150589364-aa6d69b8-9553-4cf4-a975-2c6a8ad0c77c.png)

You can also Stop or Pause the playback, or skip the current song.
You can see how much time is remaining and you can control the volume.

![image](https://user-images.githubusercontent.com/58821835/150590072-74710a3b-5efa-48ee-9f50-7d0840e375e9.png)
