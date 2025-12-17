import os
import sys
from tkinter import PhotoImage

from PIL import Image, ImageTk

from managers.settings_manager import SetttingsManager


class ImageManager:
    def __init__(self, path: str, settings_manager: SetttingsManager) -> None:
        self.images = {}
        self.path = path
        self.settings_manager = settings_manager

        self.load_images()

    def __color_image(self, image_name, color):
        color = color.lstrip("#")
        color = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))

        img = Image.open(os.path.join(self.path, image_name)).convert("RGBA")

        _, _, _, alpha = img.split()
        recolored_img = Image.new("RGBA", img.size, color + (255,))
        recolored_img.putalpha(alpha)

        return recolored_img

    def load_images(self):
        color = self.settings_manager.settings["txt_color"]

        if getattr(sys, "frozen", False):
            assert False, "Still needs to be implemented"
        else:
            self.images["stop"] = ImageTk.PhotoImage(
                self.__color_image("stop_img.png", color)
            )
            self.images["skip"] = ImageTk.PhotoImage(
                self.__color_image("skip_img.png", color)
            )
            self.images["pause"] = ImageTk.PhotoImage(
                self.__color_image("pause_img.png", color)
            )
            self.images["play"] = ImageTk.PhotoImage(
                self.__color_image("play_img.png", color)
            )
            self.images["plus"] = ImageTk.PhotoImage(
                self.__color_image("plus_img.png", color)
            )
            self.images["minus"] = ImageTk.PhotoImage(
                self.__color_image("minus_img.png", color)
            )
            self.images["gear"] = ImageTk.PhotoImage(
                self.__color_image("settings_img.png", color)
            )
            self.images["empty"] = PhotoImage(width=1, height=1)
            self.images["back"] = ImageTk.PhotoImage(
                self.__color_image("back_img.png", color)
            )
            self.images["delete"] = ImageTk.PhotoImage(
                self.__color_image("delete_img.png", color)
            )
