import csv
import os
import shutil
import sys
from configparser import ConfigParser

from appdirs import user_config_dir

VERSION = "0.6.0i"


class SetttingsManager:
    def __init__(self):
        self.path = user_config_dir("rpg-mt", "Gladon")
        if not os.path.isdir(self.path):
            self.create_config_dir()
        self.config = ConfigParser()

        self.settings = {}
        self.music_paths = []
        self.sfx_paths = []

        self.load_settings()
        self.load_paths()

    def load_settings(self) -> None:
        if os.path.isfile(os.path.join(self.path, "config.ini")):
            config_file = self.path + "/config.ini"
            self.config.read(config_file)

            try:
                settings_version = self.config["version"]["version"]
                if settings_version != VERSION:
                    self.__write_default_settings()

            except KeyError:
                self.__write_default_settings()

            self.settings = {}
            for setting in self.config["app_settings"].keys():
                self.settings[setting] = int(self.config["app_settings"][setting])

            for setting in self.config["color_settings"].keys():
                self.settings[setting] = self.config["color_settings"][setting]

        else:
            self.__write_default_settings()
            self.load_settings()

    def store_settings(self) -> None:
        for setting in self.config["app_settings"].keys():
            self.config["app_settings"][setting] = str(self.settings[setting])

        for setting in self.config["color_settings"].keys():
            self.config["color_settings"][setting] = str(self.settings[setting])

        with open(self.path + "/config.ini", "w") as configfile:
            self.config.write(configfile)

    def create_config_dir(self) -> None:
        if sys.platform.startswith("linux"):
            try:
                os.mkdir(self.path)
            except OSError:
                pass

        elif sys.platform.startswith("win32"):
            try:
                path2 = "\\".join(self.path.split("\\")[:-1])
                os.mkdir(path2)
                os.mkdir(self.path)
            except OSError:
                pass

    def reset_to_defaults(self) -> None:
        self.__write_default_settings()
        self.load_settings()

    def __write_default_settings(self):
        if getattr(sys, "frozen", False):
            path = os.path.join(sys._MEIPASS, "resources/default_config.ini")
        else:
            path = "./resources/default_config.ini"
        shutil.copyfile(
            path,
            os.path.join(self.path, "config.ini"),
        )
        self.load_settings()

    def load_paths(self):
        self.music_paths = []
        self.sfx_paths = []

        if not os.path.isfile(self.path + "/paths.csv"):
            open(self.path + "/paths.csv", "a").close()
        with open(self.path + "/paths.csv", "r", encoding="utf-8-sig") as csv_file:
            list = csv.reader(csv_file, delimiter=",", quotechar="|")
            for row in list:
                if row != []:
                    self.music_paths = row

        # --- SFX --- #
        if not os.path.isfile(self.path + "/sfx-paths.csv"):
            open(self.path + "/sfx-paths.csv", "a").close()
        with open(self.path + "/sfx-paths.csv", "r", encoding="utf-8-sig") as csv_file:
            list = csv.reader(csv_file, delimiter=",", quotechar="|")
            for row in list:
                if row != []:
                    self.sfx_paths = row

    def store_paths(self):
        # --- Music --- #
        if not os.path.isfile(self.path + "/paths.csv"):
            open(self.path + "/paths.csv", "a").close()

        for path in self.music_paths:
            try:
                with open(os.path.join(path, "songs.csv")) as _:
                    pass
            except OSError:
                try:
                    songs = open(path + "/songs.csv", "a")
                    songs.close()
                except OSError:
                    pass

        with open(self.path + "/paths.csv", "w") as csv_file:
            write = csv.writer(csv_file)
            write.writerow(self.music_paths)

        # --- SFX --- #
        if not os.path.isfile(self.path + "/sfx-paths.csv"):
            open(self.path + "/sfx-paths.csv", "a").close()

        for path in self.sfx_paths:
            try:
                with open(os.path.join(path, "sfx.csv")) as _:
                    pass
            except OSError:
                try:
                    sfxs = open(path + "/sfx.csv", "a")
                    sfxs.close()
                except OSError:
                    pass

        with open(self.path + "/sfx-paths.csv", "w") as csv_file:
            write = csv.writer(csv_file)
            write.writerow(self.sfx_paths)
