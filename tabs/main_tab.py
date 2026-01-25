import sys
import time
from tkinter import ttk
from tkinter.ttk import Progressbar, Scale, Style

from include.music_player import MusicPlayer
from include.tab import Tab
from managers.image_manager import ImageManager
from managers.settings_manager import SetttingsManager
from managers.sound_manager import SoundManager
from managers.tab_manager import TabManager


class MainTab(Tab):
    def __init__(
        self,
        settings_manager: SetttingsManager,
        tab_manager: TabManager,
        image_manager: ImageManager,
        notebook: ttk.Notebook,
        sound_manager: SoundManager,
        music_player: MusicPlayer,
    ) -> None:
        super().__init__(settings_manager, tab_manager, image_manager, notebook)
        self.sound_manager = sound_manager
        self.music_player = music_player

        self.create(True)

    def create(self, new: bool = False):
        super().create(new)

        settings = self.settings_manager.settings

        style = Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=settings["sec_bg_color"],
            background=settings["button_hov_color"],
            bordercolor=settings["sec_bg_color"],
            lightcolor="black",
            darkcolor="black",
            thickness=20 * (settings["ui_scale"] / 100),
        )

        style.configure(
            "Custom.Vertical.TScale",
            troughcolor=settings["sec_bg_color"],
            background=settings["button_hov_color"],
            lightcolor="black",
            darkcolor="black",
            sliderlength=25 * (settings["ui_scale"] / 100),
            sliderthickness=20 * (settings["ui_scale"] / 100),
            activebackground="black",
        )

        self.theme_buttons_frame = self.add_frame(self.frame)
        self.theme_buttons_frame.grid(row=1, column=0)

        self.lower_frame = self.add_frame(self.frame, bg="sec_bg_color")
        self.lower_frame.grid(row=4, column=0, pady=20)

        self.status_frame = self.add_frame(self.lower_frame, bg="sec_bg_color")
        self.status_frame.grid(row=0, column=0)

        self.volume_frame = self.add_frame(self.lower_frame, bg="sec_bg_color")
        self.volume_frame.grid(row=0, column=1)

        self.current_song_label = self.add_label(
            self.status_frame, text="No Song Playing", font_size=1.5, bg="sec_bg_color"
        )
        self.current_song_label.config(justify="left")
        self.current_song_label.grid(row=0, column=3, columnspan=2, sticky="w", padx=5)

        self.current_song_path_label = self.add_label(
            self.status_frame, text="No Song Playing", bg="sec_bg_color"
        )
        self.current_song_path_label.config(justify="left", anchor="w")
        self.current_song_path_label.grid(
            row=2, column=3, columnspan=2, sticky="w", padx=5
        )

        self.current_theme_label = self.add_label(
            self.frame, text="No Theme Selected", font_size=2
        )
        self.current_theme_label.grid(row=0, column=0, pady=10)

        self.song_duration_label = self.add_label(
            self.status_frame, text="00:00 / 00:00", bg="sec_bg_color"
        )
        # self.song_duration_label.config(width=15)
        self.song_duration_label.grid(row=1, column=4, pady=5)

        self.song_progressbar = Progressbar(
            self.status_frame,
            orient="horizontal",
            length=3 * settings["ui_scale"],
            mode="determinate",
            style="Custom.Horizontal.TProgressbar",
        )
        self.song_progressbar.grid(row=1, column=3, padx=5)

        self.__update_music_labels()

        self.volume_label = self.add_label(
            self.volume_frame,
            text=str(settings["volume"]),
            bg="sec_bg_color",
        )
        self.volume_label.config(width=3)
        self.volume_label.grid(row=2, column=1, sticky="s")

        self.stop_button = self.add_button(
            self.status_frame,
            command=self.__stop,
            image="stop",
            scale=0.7,
        )
        self.stop_button.grid(row=0, column=0, rowspan=3)

        self.pause_button = self.add_button(
            self.status_frame,
            command=self.__pause,
            image="pause",
            scale=0.7,
        )
        root = self.pause_button.winfo_toplevel()
        root.bind("<space>", self.__pause)
        self.pause_button.grid(row=0, column=1, rowspan=3)

        self.skip_button = self.add_button(
            self.status_frame,
            command=self.__skip,
            image="skip",
            scale=0.7,
        )
        self.skip_button.grid(row=0, column=2, rowspan=3)

        self.volume_changer = Scale(
            self.volume_frame,
            from_=100,
            to=0,
            orient="vertical",
            value=int(settings["volume"]),
            command=self.__change_volume,
            length=int(1.5 * settings["ui_scale"]),
            style="Custom.Vertical.TScale",
        )
        self.volume_changer.grid(row=0, column=0, rowspan=5, padx=5)

        self.volume_up_button = self.add_button(
            self.volume_frame,
            command=self.__volume_up,
            image="plus",
            scale=0.3,
        )
        self.volume_up_button.grid(row=1, column=1, pady=5)

        self.volume_down_button = self.add_button(
            self.volume_frame,
            command=self.__volume_down,
            image="minus",
            scale=0.3,
        )
        self.volume_down_button.grid(row=3, column=1, pady=5)

        self.add_navigation_button(destination="settings", image="gear")

        self.__create_theme_buttons()
        self.__create_sfx_buttons()

        self.navigation_buttons_frame.tkraise()

        self.__song_duration()

    def __create_theme_buttons(self):
        settings = self.settings_manager.settings
        self.theme_buttons = {}

        i = 0
        for _theme in sorted(self.sound_manager.themes.keys()):
            theme_button = self.add_button(
                self.theme_buttons_frame,
                text=_theme,
                scale=settings["theme_button_scale"] * 0.5,
                command=lambda _theme=_theme: self.__play(_theme),
                wraplength=settings["ui_scale"],
            )
            theme_button.grid(
                row=(i // settings["row_length"] + 1),
                column=(i % settings["row_length"]),
            )

            if self.music_player.theme == _theme:
                theme_button.config(bg=settings["button_hov_color"], relief="sunken")

            i += 1
            self.theme_buttons[_theme] = theme_button

    def __create_sfx_buttons(self):
        if not self.settings_manager.settings["sfx_tab"] == 1:
            return

        settings = self.settings_manager.settings

        self.sfx_button_frame = self.add_label_frame(self.frame)
        self.sfx_button_frame.grid(row=6, column=0)

        self.sfx_label = self.add_label(
            self.frame,
            text="Sound Effects",
            font_size=1.5,
        )
        self.sfx_label.grid(row=5, column=0, pady=5)

        sfx_list = self.sound_manager.get_sfx_list()
        self.sfx_buttons = []

        i = 0
        for sfx in sfx_list:
            text = ""
            if sys.platform.startswith("win32"):
                text = sfx.split("\\")
                text = text[-1].split(".mp3")[0]

            elif sys.platform.startswith("linux"):
                text = sfx.split("/")
                text = text[-1].split(".mp3")[0]

            sfx_button = self.add_button(
                self.sfx_button_frame,
                text=text,
                scale=settings["theme_button_scale"] * 0.5,
                command=lambda sfx=sfx: self.music_player.play_sfx(sfx),
                wraplength=settings["ui_scale"],
            )
            sfx_button.grid(
                row=(i // settings["row_length"] + 1),
                column=(i % settings["row_length"]),
            )

            i += 1

    def __play(self, theme):
        self.theme_buttons[theme].config(
            bg=self.settings_manager.settings["button_hov_color"], relief="sunken"
        )

        if self.music_player.theme is not None and not theme == self.music_player.theme:
            self.theme_buttons[self.music_player.theme].config(
                bg=self.settings_manager.settings["button_bg_color"], relief="raised"
            )

        self.music_player.change_theme(theme)
        self.__update_music_labels()

    def __stop(self):
        if self.music_player.theme is None:
            return

        self.theme_buttons[self.music_player.theme].config(
            bg=self.settings_manager.settings["button_bg_color"], relief="raised"
        )
        self.song_duration_label.config(text="00:00 / 00:00")

        self.music_player.stop()
        self.__update_music_labels()

    def __skip(self):
        self.music_player.skip()
        self.__update_music_labels()

    def __pause(self, space_key=None):
        if self.music_player.paused:
            self.pause_button.config(image=self.image_manager.images["pause"])
        else:
            self.pause_button.config(image=self.image_manager.images["play"])

        self.music_player.pause()

    def __song_duration(self):
        if not self.music_player.paused:
            length = self.music_player.length
            # if the track is longer than 1 hour, we display the hours
            # As most tracks will likely be shorter, we usually only display minutes and seconds
            if length >= 3600:
                format = "%H:%M:%S"
            else:
                format = "%M:%S"

            current_time = self.music_player.get_pos()
            converted_current_time = time.strftime(format, time.gmtime(current_time))

            if current_time >= length and not self.music_player.paused:
                self.music_player.play()
                self.__update_music_labels()

                # We set this explicitly to make sure we don't get something like 01:12 / 01:05, which can happen for 1 tick
                converted_current_time = time.strftime(format, time.gmtime(0))

            converted_length = time.strftime(format, time.gmtime(length))
            song_time = str(converted_current_time) + " / " + str(converted_length)

            self.song_duration_label.config(text=song_time)
            self.song_progressbar["value"] = current_time / length * 100

        self.song_duration_label.after(100, self.__song_duration)

    def __update_music_labels(self):
        if not self.music_player.is_playing():
            self.current_theme_label.config(text="No Theme Selected")
            self.current_song_label.config(text="No Song Playing")
            self.current_song_path_label.config(text="No Song Playing")

            self.song_duration_label.config(text="00:00 / 00:00")
            self.song_progressbar["value"] = 0

        else:
            song = ""
            path = ""
            if sys.platform.startswith("linux"):
                song = self.music_player.song.split("/")[-1].split(".mp3")[0]
                path = self.music_player.song.split("/")[-2]

            elif sys.platform.startswith("win32"):
                song = self.music_player.song.split("\\")[-1].split(".mp3")[0]
                path = self.music_player.song.split("\\")[-2]

            if self.settings_manager.settings["full_paths_main"]:
                path = self.music_player.song

            max_base_song_length = 30
            max_song_length = (
                max_base_song_length
                * (self.settings_manager.settings["ui_scale"] / 100)
                * (12 / self.settings_manager.settings["font_size"])
            )
            max_song_length = int(max_song_length)
            if len(song) > max_song_length:
                song = song[:max_song_length] + "..."

            self.current_theme_label.config(text=str(self.music_player.theme))
            self.current_song_label.config(text=song)
            self.current_song_path_label.config(text=path)

    def __change_volume(self, pos):
        self.__set_volume(int(float(pos)))

    def __volume_up(self):
        volume = self.settings_manager.settings["volume"] + 1
        self.__set_volume(volume, True)

    def __volume_down(self):
        volume = self.settings_manager.settings["volume"] - 1
        self.__set_volume(volume, True)

    def __set_volume(self, volume: int, button: bool = False):
        self.settings_manager.settings["volume"] = volume
        self.settings_manager.store_settings()

        self.volume_label.config(text=str(int(volume)))
        if button:
            self.volume_changer.set(volume)
        self.music_player.set_volume()
