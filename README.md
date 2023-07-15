# RPG-Music-Tool (ver. 0.6.dev)

==DEV BRANCH==

- **[Installation](#installation)**
	- [Windows and Linux](#windows-and-linux)
	- [Mac (not supported for now)](#mac)
	- [General](#general)
- **[Setup](#setup)**
	- [1. Paths](#1-paths)
	- [2. Themes](#2-themes)
	- [3. Start using](#3-start-using)
- **[Settings and Customisation](#settings-and-customisation)**


A small music tool for TTRPGs.

This Tool allows you to play music based on the current theme or setting for your TableTop RolePlayingGames. \
This Program uses local music files, instead of for example a Spotify Playlist. So you can always use it as long as you have your music with you.

## Installation
### Windows and Linux
**Use the Executable**
Download the executable for your system from the Release section. \
(Windows executables are only put up with "major" versions.)

### Mac
**Mac is not officially supported**

### General
You can always download the repo and execute the python file.


## Setup
After downloading the application open it. It only takes a few steps to get ready. Have some music and sound effects ready you want to use. This app only works with mp3 files at the moment, so make sure your files are in mp3 format.\
(If at any point something doesn't appear to work, restart the app, that fixes most things)

### 1 Paths
In the App open the "Paths" Tab and your directory paths. \
Simply separate multiple paths with a line break. Your sound effect (SFX) will be displayed with their title, so make sure to name the files are named a way you know what they are about. \

For Linux they should look something like:
```
/home/[username]/Music/D&D-Combat/
/home/[username]/Music/D&D-Travel/
```

And for Windows:
```
C:\Users\[Username]\Music\D&D-Combat\
C:\Users\[Username]\Music\D&D-Travel\
```

If something is wrong with your path, it will be highlighted red.\
The app will also create a file in the selected directories called "songs.csv". This keeps track of the songs in said directory and the set themes (See next section) will be saved there. That also means you can easily transfer songs with their themes from one computer to another, by copying the directories.

### 2 Themes
After adding the paths, open the "Song Themes" Tab.\
There all the paths you added should be listed (If not a restart should fix that). There you can go through all songs and categorize them in themes according to your tastes.\
A single song can be assign multiple themes, just separate them with a semicolon (";"). You can play the song in this tab, with the little play icon next to the song.\
If you later select a theme to be played, the app will select songs assigned to this theme by random.

### 3 Start using
Go back to the main tab and start using the app.
![Screenshot from 2022-12-07 23-24-33](https://user-images.githubusercontent.com/58821835/206310072-63aadbe7-1e9e-4bd2-9f9f-a94319011e1e.png)



## Settings and Customisation
You can change a few things about the app in the "Settings" Tab\
![Screenshot from 2022-12-07 23-25-00](https://user-images.githubusercontent.com/58821835/206310022-97a702fd-ec88-4230-8bab-e6c4f6909336.png)


## Building yourself
Should you want to build the app yourself or want to run the python file directly, you need to install the dependencies first:
Linux: 
```sh
pip install -r requirements_linux.txt
```
Windows:
```sh
pip install -r requirements_win.txt
```
(An additial package specific to Windows is included)
Also make sure you have tkinter installed. This should usually be bundled into your python distribution, but if not, just search the web for a solution.

After the dependencies are installed, you can start the app by running:
```sh
python main.py
```

To make it an executable yourself, you can run the build script:
Linux:
```sh
./build.sh -o <filename>
```
Windows:
```sh
build.bat -o <filename>
```
The script runs the appropriate `pyinstaller` command (which is automatically installed, if missing). 
The executable will then compile for the platform you run the command on. You will find it in the "dist" directory.
You can also just run `pyinstaller` by yourself, for more info on that just visit its [documentation](https://pyinstaller.org/).
