import sys
from tkinter import END, Button, Frame, Label, ttk

from include.music_player import MusicPlayer
from include.predictive_text import PredictiveText
from include.tab import Tab
from managers.image_manager import ImageManager
from managers.settings_manager import SetttingsManager
from managers.sound_manager import SoundManager
from managers.tab_manager import TabManager


class ThemesTab(Tab):
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

        self.page_number = 0
        self.songs_per_page = self.settings_manager.settings["rows_per_page"]
        self.current_song_playing = None

        self.create(new=True)

    def __select_tab(self, tab):
        for predictive_text in self.theme_boxes:
            if predictive_text.predict_label is not None:
                predictive_text.predict_label.destroy()
                predictive_text.predict_label = None
            if predictive_text.predict_popup is not None:
                predictive_text.predict_popup.destroy()
                predictive_text.predict_popup = None

        self.__apply_added_themes_page_change()
        self.tab_manager.update("main")
        self.tab_manager.select(tab)

    def add_navigation_button(self, destination: str, image: str) -> Button:
        navigation_button = super().add_navigation_button(destination, image)

        navigation_button.config(command=lambda: self.__select_tab(destination))

        return navigation_button

    def create(self, new: bool = False):
        super().create(new)

        settings = self.settings_manager.settings
        self.paths = self.settings_manager.music_paths

        self.current_path_index = 0

        self.top_display_frame = self.add_frame(self.frame, bg="sec_bg_color")
        self.top_display_frame.grid(row=1, column=0)

        self.list_frame = self.add_frame(self.frame)
        self.list_frame.grid(row=2, column=0, pady=10, padx=10, sticky="n")

        self.page_navigation_frame = self.add_frame(self.frame)
        self.page_navigation_frame.grid(row=3, column=0)

        # --- Labels --- #
        self.label_title_themes = self.add_label(
            self.frame,
            text="Music Themes",
            font_size=2,
        )
        self.label_title_themes.grid(row=0, column=0, pady=5)

        directory_label_string = self.__create_directory_label_string()
        self.label_current_directory = self.add_label(
            self.top_display_frame, text=directory_label_string, bg="sec_bg_color"
        )
        self.label_current_directory.config(width=int(0.4 * settings["ui_scale"]))
        self.label_current_directory.grid(row=0, column=1)

        self.add_navigation_button(destination="settings", image="back")

        self.previous_path_button = self.add_button(
            self.top_display_frame,
            image="left",
            command=self.__previous_path,
            scale=0.35,
        )
        self.previous_path_button.grid(row=0, column=0, padx=5)
        if self.current_path_index == 0:
            self.previous_path_button.config(state="disabled")

        self.next_path_button = self.add_button(
            self.top_display_frame,
            image="right",
            command=self.__next_path,
            scale=0.35,
        )
        self.next_path_button.grid(row=0, column=2, padx=5)
        if len(self.paths) == 0 or (self.current_path_index + 1) == len(self.paths):
            self.next_path_button.config(state="disabled")

        self.__create_list()

        self.previous_page_button = self.add_button(
            self.list_frame,
            image="up",
            command=self.__previous_page,
            scale=0.35,
        )
        self.previous_page_button.grid(row=0, column=3, sticky="e", padx=5)
        if self.page_number == 0:
            self.previous_page_button.config(state="disabled")

        self.next_page_button = self.add_button(
            self.list_frame,
            image="down",
            command=self.__next_page,
            scale=0.35,
        )
        self.next_page_button.grid(
            row=self.songs_per_page - 1, column=3, sticky="w", padx=5
        )
        if len(self.paths) == 0 or (self.page_number + 1) * self.songs_per_page >= len(
            list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())
        ):
            self.next_page_button.config(state="disabled")

    def __create_list(self):
        if len(self.paths) == 0:
            return

        settings = self.settings_manager.settings
        songs = list(
            self.sound_manager.songs[self.paths[self.current_path_index]].keys()
        )
        per_page = self.songs_per_page
        page = self.page_number
        self.entryframes: list[Frame] = []
        self.play_buttons: list[Button] = []
        self.theme_boxes: list[PredictiveText] = []
        self.songs_labels: list[Label] = []

        songs_in_path = len(songs)
        remaining_paths = songs_in_path - per_page * page
        for i in range(min(per_page, remaining_paths)):
            index_with_offset = per_page * page + i
            song = songs[index_with_offset]

            color = "bg_color" if i % 2 == 1 else "sec_bg_color"

            entry_frame = self.add_frame(self.list_frame, bg=color)

            song_play_button = self.add_button(
                entry_frame,
                image="play_small",
                command=lambda i=index_with_offset: self.__play(i),
                scale=0.25,
            )
            song_play_button.grid(row=0, column=0, pady=2, padx=10)

            song_label = self.add_label(
                entry_frame,
                text=song,
                bg=color,
            )
            song_label.config(width=int(0.35 * settings["ui_scale"]))
            song_label.grid(row=0, column=1)

            song_themes = PredictiveText(
                entry_frame,
                self.sound_manager.get_themes_list(),
                "#",
                width=int(settings["ui_scale"] * 0.4),
                height=int(3 * settings["ui_scale"] / 100),
                bg=settings[color],
                font=("Helvetica", settings["font_size"]),
            )
            self.widgets.append(song_themes)
            song_themes.myId = song
            song_themes.grid(row=0, column=2, padx=10)
            song_themes.insert(
                "1.1",
                " #".join(
                    self.sound_manager.songs[self.paths[self.current_path_index]][song]
                ),
            )
            if (
                len(self.sound_manager.songs[self.paths[self.current_path_index]][song])
                != 0
            ):
                song_themes.insert(END, " #")
            song_themes.bind("<FocusOut>", self.__apply_added_themes_focus_out, add="+")

            self.play_buttons.append(song_play_button)
            self.theme_boxes.append(song_themes)
            self.songs_labels.append(song_label)
            self.entryframes.append(entry_frame)

            entry_frame.grid(row=i, column=0)

    def __apply_added_themes_focus_out(self, event):
        new_themes = event.widget.get_added_tags()
        song_themes = event.widget.get_tags()
        path = self.paths[self.current_path_index]
        song = event.widget.myId

        self.__apply_added_themes(path, song, new_themes, song_themes)

    def __apply_added_themes_page_change(self):
        for i in range(len(self.play_buttons)):
            current_focus = self.theme_boxes[i].focus_get()
            if current_focus == self.theme_boxes[i]:
                path = self.paths[self.current_path_index]
                song = self.theme_boxes[i].myId
                new_themes = self.theme_boxes[i].get_added_tags()
                song_themes = self.theme_boxes[i].get_tags()
                self.__apply_added_themes(path, song, new_themes, song_themes)

    def __apply_added_themes(self, path, song, new_themes, song_themes):
        if new_themes != []:
            self.sound_manager.add_new_themes(new_themes)

        self.sound_manager.change_song_themes(path, song, song_themes)

        new_possible_themes = self.sound_manager.get_themes_list() + new_themes
        for text in self.theme_boxes:
            if text is None:
                continue
            text.update_possible_tags(new_possible_themes)

        self.sound_manager.store_themes()

    def __destroy_list(self):
        for i in range(len(self.play_buttons)):
            self.entryframes[i].destroy()
            self.play_buttons[i].destroy()
            self.theme_boxes[i].destroy()
            self.songs_labels[i].destroy()

    def __play(self, i):
        index_in_list = i % self.songs_per_page
        if index_in_list == self.current_song_playing:
            self.__stop()
            return

        if self.current_song_playing is not None:
            self.play_buttons[self.current_song_playing].config(
                image=self.image_manager.images["play_small"]
            )

        self.current_song_playing = index_in_list
        self.play_buttons[index_in_list].config(
            image=self.image_manager.images["stop_small"]
        )

        song_path = (
            self.paths[self.current_path_index]
            + list(
                self.sound_manager.songs[self.paths[self.current_path_index]].keys()
            )[i]
        )

        self.music_player.stop()
        self.music_player.play(song_path)

    def __stop(self):
        if self.current_song_playing is not None:
            self.play_buttons[self.current_song_playing].config(
                image=self.image_manager.images["play_small"]
            )

        self.current_song_playing = None
        self.music_player.stop()

    def __create_directory_label_string(self):
        if len(self.paths) == 0:
            return "No Paths added yet, go to the paths settings to do so"

        path_string = ""

        if self.settings_manager.settings["full_paths_settings"]:
            path_string = self.paths[self.current_path_index]

        elif sys.platform.startswith("linux"):
            path_string = self.paths[self.current_path_index].split("/")[-2]

        elif sys.platform.startswith("win32"):
            path_string = self.paths[self.current_path_index].split("\\")[-2]

        return path_string

    def __previous_page(self):
        self.__apply_added_themes_page_change()
        self.page_number -= 1
        if self.page_number == 0:
            self.previous_page_button.config(state="disabled")
        if not (self.page_number + 1) * self.songs_per_page >= len(
            list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())
        ):
            self.next_page_button.config(state="active")

        self.__stop()
        self.__destroy_list()
        self.__create_list()

    def __next_page(self):
        self.__apply_added_themes_page_change()
        self.page_number += 1
        if (self.page_number + 1) * self.songs_per_page >= len(
            list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())
        ):
            self.next_page_button.config(state="disabled")
        if not self.page_number == 0:
            self.previous_page_button.config(state="active")

        self.__stop()
        self.__destroy_list()
        self.__create_list()

    def __previous_path(self):
        self.__apply_added_themes_page_change()
        self.current_path_index -= 1

        if self.current_path_index == 0:
            self.previous_path_button.config(state="disabled")
        if not (self.current_path_index + 1) == len(self.paths):
            self.next_path_button.config(state="active")

        self.__set_directory()

    def __next_path(self):
        self.__apply_added_themes_page_change()
        self.current_path_index += 1
        if (self.current_path_index + 1) == len(self.paths):
            self.next_path_button.config(state="disabled")
        if not self.current_path_index == 0:
            self.previous_path_button.config(state="active")
        self.__set_directory()

    def __set_directory(self):
        directory_label_string = self.__create_directory_label_string()
        self.label_current_directory.config(text=directory_label_string)

        self.page_number = 0
        self.previous_page_button.config(state="disabled")
        self.next_page_button.config(state="disabled")
        if not (self.page_number + 1) * self.songs_per_page >= len(
            list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())
        ):
            self.next_page_button.config(state="active")

        self.__stop()
        self.__destroy_list()
        self.__create_list()

    def update(self):
        super().update()
        self.songs_per_page = self.settings_manager.settings["rows_per_page"]
