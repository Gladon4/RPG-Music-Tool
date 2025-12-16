import csv
import os


class SoundManager:
    def __init__(self, set_manager):
        self.set_manager = set_manager

        self.load_themes()
        self.load_sfx()

    # --- Themes --- #
    def load_themes(self):
        self.themes = {}
        self.songs = {}

        try:
            for path in self.set_manager.music_paths:
                self.songs[path] = {}

                with open(path + "/songs.csv", "r", encoding="utf-8-sig") as csv_file:
                    list = csv.reader(csv_file, delimiter="\\", quotechar="|")
                    for row in list:
                        if not row[0] == "":
                            self.songs[path][row[0]] = []

                        if len(row) >= 2:
                            for theme in row[1].split(";"):
                                if not theme == "":
                                    self.songs[path][row[0]].append(theme)

        except IOError:
            pass

        self.check_for_new_files()
        self.create_themes_dict()

    def check_for_new_files(self):
        for path in self.set_manager.music_paths:
            for file in os.listdir(path):
                if file not in self.songs[path] and file.endswith(".mp3"):
                    print(f"New Song found: {file}")
                    self.songs[path][file] = []

            removed_songs = []
            for song in self.songs[path]:
                if song not in os.listdir(path):
                    print(f"Deleted File found: {song}")
                    removed_songs.append(song)

            for song in removed_songs:
                self.songs[path].pop(song, None)

        self.store_themes()

    def create_themes_dict(self):
        self.themes = {}
        for path in self.set_manager.music_paths:
            for song in self.songs[path]:
                for theme in self.songs[path][song]:
                    if theme not in self.themes:
                        self.themes[theme] = []

                    self.themes[theme].append(path + song)

    def get_themes_list(self):
        return list(self.themes.keys())

    def add_new_themes(self, themes):
        for theme in themes:
            self.themes[theme] = []

    def change_song_themes(self, path, song, themes):
        if self.songs[path][song] == themes:
            return

        self.songs[path][song] = themes
        self.create_themes_dict()

    def store_themes(self):
        try:
            for path in self.set_manager.music_paths:
                rows = []

                for song in self.songs[path]:
                    themes = ""
                    for theme in self.songs[path][song]:
                        themes += theme + ";"

                    rows.append([song, themes])

                with open(path + "songs.csv", "w", newline="") as file:
                    csvwriter = csv.writer(file, delimiter="\\")
                    csvwriter.writerows(rows)

        except IOError:
            pass

    # --- SFX --- #
    def load_sfx(self):
        self.sfxs = {}

        try:
            for path in self.set_manager.sfx_paths:
                self.sfxs[path] = []

                with open(path + "/sfx.csv", "r", encoding="utf-8-sig") as csv_file:
                    list = csv.reader(csv_file, delimiter="\\", quotechar="|")
                    for row in list:
                        if not row[0] == "":
                            self.sfxs[path] += [row[0]]
        except IOError:
            pass

    def store_sfx(self):
        try:
            for path in self.set_manager.sfx_paths:
                rows = []

                for song in self.sfxs[path]:
                    rows.append([song])

                with open(path + "sfx.csv", "w", newline="") as file:
                    csvwriter = csv.writer(file, delimiter="\\")
                    csvwriter.writerows(rows)

        except IOError:
            pass
