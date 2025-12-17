from tkinter import Tk, ttk

from include.player import MusicPlayer
from managers.image_manager import ImageManager
from managers.settings_manager import SetttingsManager
from managers.sound_manager import SoundManager
from managers.tab_manager import TabManager
from tabs.main_tab import MainTab
from tabs.paths_tab import PathsTab
from tabs.settings_tab import SettingsTab
from tabs.sfx_tab import SFXTab
from tabs.themes_tab import ThemesTab


class App:
    def __init__(self, app_name, start_size) -> None:
        self.app_name = app_name

        self.root = Tk()
        self.style = ttk.Style()
        self.notebook = ttk.Notebook(self.root)

        self.root.title(app_name)
        self.root.geometry(start_size)

        self.style.layout("TNotebook.Tab", [])
        self.notebook.pack(fill="both", expand=1)

        self.settings_manager = SetttingsManager()
        self.sound_manager = SoundManager(self.settings_manager)
        self.player = MusicPlayer(self.settings_manager, self.sound_manager)
        self.image_manager = ImageManager("img", self.settings_manager)
        self.tab_manager = TabManager(self.notebook, self.image_manager)

        self.main_tab = MainTab(
            self.settings_manager,
            self.tab_manager,
            self.image_manager,
            self.notebook,
            self.sound_manager,
            self.player,
        )
        self.settings_tab = SettingsTab(
            self.settings_manager, self.tab_manager, self.image_manager, self.notebook
        )
        self.paths_tab = PathsTab(
            self.settings_manager, self.tab_manager, self.notebook, self.sound_manager
        )
        self.sfx_tab = SFXTab(
            self.settings_manager, self.tab_manager, self.notebook, self.sound_manager
        )
        self.themes_tab = ThemesTab(
            self.settings_manager,
            self.sound_manager,
            self.tab_manager,
            self.notebook,
            self.player,
        )

        self.notebook.add(self.main_tab.frame, text="Main")

        self.notebook.add(self.settings_tab.frame, text="Settings")

        self.paths_tab.create()
        self.notebook.add(self.paths_tab.frame, text="Song Paths")

        self.sfx_tab.create()
        self.notebook.add(self.sfx_tab.frame, text="SFX Paths")

        self.themes_tab.create()
        self.notebook.add(self.themes_tab.frame, text="Themes")

        self.tab_manager.set_tabs(
            {
                "main": self.main_tab,
                "settings": self.settings_tab,
                "song_paths": self.paths_tab,
                "sfx_paths": self.sfx_tab,
                "themes": self.themes_tab,
            }
        )

    def run(self):
        print(f"\n --- {self.app_name} --- \n")

        self.root.mainloop()
