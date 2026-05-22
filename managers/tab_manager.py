from tkinter import ttk

from managers.image_manager import ImageManager


class TabManager:
    def __init__(self, notebook: ttk.Notebook, image_manager: ImageManager):
        self.notebook = notebook
        self.tabs = {}
        self.image_manager = image_manager

    def set_tabs(self, tabs):
        self.tabs = tabs

    def select(self, tab):
        sel = self.tabs[tab]
        self.notebook.select(sel.frame)

    def update(self, tab):
        if tab not in self.tabs:
            return
        self.tabs[tab].update()

    def update_all_tab_elements(self):
        self.image_manager.load_images()

        for tab in self.tabs:
            self.tabs[tab].update()
