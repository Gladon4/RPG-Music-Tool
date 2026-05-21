import os
import sys
from tkinter import ttk

import tkfilebrowser

from include.tab import Tab
from managers.image_manager import ImageManager
from managers.settings_manager import SetttingsManager
from managers.sound_manager import SoundManager
from managers.tab_manager import TabManager

if sys.platform.startswith("win32"):
    # Required on windows for tkfilebrowser
    import win32com


class PathsTab(Tab):
    def __init__(
        self,
        settings_manager: SetttingsManager,
        tab_manager: TabManager,
        image_manager: ImageManager,
        notebook: ttk.Notebook,
        sound_manager: SoundManager,
    ):
        super().__init__(settings_manager, tab_manager, image_manager, notebook)

        self.sound_manager = sound_manager

        self.page_number = 0
        self.paths_per_page = self.settings_manager.settings["rows_per_page"]
        self.paths = {}

        self.create(True)

    def create(self, new=False):
        super().create(new)
        ui_scale = self.settings_manager.settings["ui_scale"]

        self.list_frame = self.add_frame(self.frame)
        self.list_frame.config(width=1000)
        self.list_frame.grid(row=1, column=0, pady=10, sticky="n")

        self.page_navigation_frame = self.add_frame(self.list_frame)
        self.page_navigation_frame.grid(row=self.paths_per_page + 1, column=0)
        self.page_navigation_frame.grid_columnconfigure(1, minsize=350)

        self.frame.grid_rowconfigure(1, minsize=500)

        self.label_title_paths = self.add_label(
            self.frame,
            text="Music Directories",
            font_size=2,
        )
        self.label_title_paths.grid(row=0, column=0, pady=5)

        self.add_navigation_button(destination="sfx_paths", image="note1")
        self.add_navigation_button(destination="settings", image="back")

        self.add_path_button = self.add_button(
            self.page_navigation_frame,
            text="Add Music Directory",
            command=self.__music_path_picker,
            wraplength=1 * ui_scale,
        )
        self.add_path_button.config(width=1 * ui_scale, height=0.5 * ui_scale)
        self.add_path_button.grid(row=0, column=1)

        self.previous_page_button = self.add_button(
            self.page_navigation_frame,
            image="left",
            command=self.__previous_page,
            scale=0.35,
        )
        self.previous_page_button.grid(row=0, column=0)
        if self.page_number == 0:
            self.previous_page_button.config(state="disabled")

        self.next_page_button = self.add_button(
            self.page_navigation_frame,
            image="right",
            command=self.__next_page,
            scale=0.35,
        )
        self.next_page_button.grid(row=0, column=2)
        if (self.page_number + 1) * self.paths_per_page >= len(
            self.settings_manager.music_paths
        ):
            self.next_page_button.config(state="disabled")

        self.__create_list()

    def __create_list(self):
        settings = self.settings_manager.settings
        per_page = self.paths_per_page
        page = self.page_number

        requested_widths = []

        rmaining_paths = len(self.settings_manager.music_paths) - per_page * page
        for i in range(min(per_page, rmaining_paths)):
            index_with_offset = per_page * page + i
            path = self.settings_manager.music_paths[index_with_offset]

            color = "bg_color" if i % 2 == 1 else "sec_bg_color"

            entry_frame = self.add_frame(self.list_frame, bg=color)

            path_delete_button = self.add_button(
                entry_frame,
                image="delete",
                command=lambda i=index_with_offset: self.__delete(i),
                scale=0.4,
            )
            path_delete_button.grid(row=0, column=0, pady=2)

            path_text = ""
            if settings["full_paths_settings"]:
                path_text = path

            elif sys.platform.startswith("linux"):
                path_text = path.split("/")[-2]

            elif sys.platform.startswith("win32"):
                path_text = path.split("\\")[-2]

            path_label = self.add_label(
                entry_frame,
                text=path_text,
                bg=color,
                wraplength=5 * settings["ui_scale"],
            )
            requested_widths.append(path_label.winfo_reqwidth())
            path_label.config(anchor="w")
            path_label.grid(row=0, column=1, padx=5)

            entry_frame.grid(row=i, column=0)
            self.paths[i] = [entry_frame, path_delete_button, path_label]

        base_max_width = 5 * settings["ui_scale"]
        # If you set the width of the label, the requested width in pixels is ~1.35 the font size
        # I have no idea why, but we use the convertion factor, 1/1.35 ~ 0.75
        max_width = min(base_max_width, max(requested_widths)) / (
            0.75 * settings["font_size"]
        )
        max_width = int(max_width) + 1  # +1 to prevent weird cutoff with the wrapping
        for path in self.paths:
            self.paths[path][2].config(width=max_width)

    def __next_page(self):
        self.__destroy_list()

        self.page_number += 1
        self.__create_list()

        if (self.page_number + 1) * self.paths_per_page >= len(
            self.settings_manager.music_paths
        ):
            self.next_page_button.config(state="disabled")
        if not self.page_number == 0:
            self.previous_page_button.config(state="active")

    def __previous_page(self):
        self.__destroy_list()

        self.page_number -= 1
        self.__create_list()

        if self.page_number == 0:
            self.previous_page_button.config(state="disabled")
        if not (self.page_number + 1) * self.paths_per_page >= len(
            self.settings_manager.music_paths
        ):
            self.next_page_button.config(state="active")

    def __music_path_picker(self):
        dirs = tkfilebrowser.askopendirnames(
            title="Select your Music Directories",
            initialdir=os.path.expanduser("~"),
            okbuttontext="Select",
        )

        self.settings_manager.music_paths += [
            dir + "/" if sys.platform.startswith("linux") else dir + "\\"
            for dir in dirs
        ]

        self.__destroy_list()
        self.__create_list()

        self.settings_manager.store_paths()
        self.sound_manager.load_themes()

    def __delete(self, index):
        self.settings_manager.music_paths = (
            self.settings_manager.music_paths[:index]
            + self.settings_manager.music_paths[index + 1 :]
        )
        self.__destroy_list()
        self.__create_list()

        self.settings_manager.store_paths()
        self.sound_manager.load_themes()

        if (self.page_number + 1) * self.paths_per_page >= len(
            self.settings_manager.music_paths
        ):
            self.next_page_button.config(state="disabled")

        self.tab_manager.update("main")
        self.tab_manager.update("themes")

    def __destroy_list(self):
        for path in self.paths:
            self.paths[path][0].destroy()
            self.paths[path][1].destroy()
            self.paths[path][2].destroy()
        self.paths = {}

    def destroy(self):
        super().destroy()
        self.__destroy_list()

    def update(self):
        super().update()
        self.paths_per_page = self.settings_manager.settings["rows_per_page"]
