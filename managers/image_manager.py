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

    def __color_image(self, image_name, color) -> Image.Image:
        color = color.lstrip("#")
        color = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))

        img = Image.open(os.path.join(self.path, image_name)).convert("RGBA")

        _, _, _, alpha = img.split()
        recolored_img = Image.new("RGBA", img.size, color + (255,))
        recolored_img.putalpha(alpha)

        return recolored_img

    def __scale_image(self, image: Image.Image, scale: float) -> Image.Image:
        return image.resize((int(image.size[0] * scale), int(image.size[1] * scale)))

    def __invert_hex_color(self, hex_color):
        hex_color = hex_color.lstrip("#")

        r = 255 - int(hex_color[0:2], 16)
        g = 255 - int(hex_color[2:4], 16)
        b = 255 - int(hex_color[4:6], 16)

        return f"#{r:02x}{g:02x}{b:02x}"

    def load_images(self):
        color = self.settings_manager.settings["txt_color"]
        scale = self.settings_manager.settings["ui_scale"] / 100

        if getattr(sys, "frozen", False):
            assert False, "Still needs to be implemented"
        else:
            self.images["stop"] = ImageTk.PhotoImage(
                self.__scale_image(self.__color_image("stop_img.png", color), scale),
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
            self.images["check_on"] = ImageTk.PhotoImage(
                self.__color_image("check_on.png", color).resize((32, 32))
            )
            self.images["check_off"] = ImageTk.PhotoImage(
                self.__color_image("check_off.png", color).resize((32, 32))
            )
            self.images["eyedropper"] = ImageTk.PhotoImage(
                self.__color_image("eyedropper.png", color)
            )
            self.images["eyedropper_inverse"] = ImageTk.PhotoImage(
                self.__color_image("eyedropper.png", self.__invert_hex_color(color))
            )
            self.images["label"] = ImageTk.PhotoImage(
                self.__color_image("label.png", color)
            )
            self.images["delete"] = ImageTk.PhotoImage(
                self.__color_image("delete_img.png", color)
            )
            self.images["list"] = ImageTk.PhotoImage(
                self.__color_image("list_img.png", color)
            )
