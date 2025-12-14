import os
import sys
from tkinter import PhotoImage


class ImageManager:
    def __init__(self, path: str) -> None:
        self.images = {}
        self.path = path

        if getattr(sys, "frozen", False):
            assert False, "Still needs to be implemented"
        else:
            self.images["stop"] = PhotoImage(
                file=os.path.join(self.path, "stop_img.png")
            )
            self.images["skip"] = PhotoImage(
                file=os.path.join(self.path, "skip_img.png")
            )
            self.images["pause"] = PhotoImage(
                file=os.path.join(self.path, "pause_img.png")
            )
            self.images["play"] = PhotoImage(
                file=os.path.join(self.path, "play_img.png")
            )
            self.images["plus"] = PhotoImage(
                file=os.path.join(self.path, "plus_img.png")
            )
            self.images["minus"] = PhotoImage(
                file=os.path.join(self.path, "minus_img.png")
            )
            self.images["gear"] = PhotoImage(
                file=os.path.join(self.path, "settings_img.png")
            )
            self.images["empty"] = PhotoImage(width=1, height=1)
            self.images["back"] = PhotoImage(
                file=os.path.join(self.path, "back_img.png")
            )
            self.images["delete"] = PhotoImage(
                file=os.path.join(self.path, "delete_img.png")
            )
