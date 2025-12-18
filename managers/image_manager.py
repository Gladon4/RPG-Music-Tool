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

    def __color_image(self, path, color) -> Image.Image:
        color = color.lstrip("#")
        color = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))

        img = Image.open(path).convert("RGBA")

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

    def __load_image(self, name, file_name=None, inverse=False, size=None):
        if file_name is None:
            file_name = name
        color = self.settings_manager.settings["txt_color"]
        if inverse:
            color = self.__invert_hex_color(color)

        scale = self.settings_manager.settings["ui_scale"] / 100

        colored_image = self.__color_image(
            os.path.join(self.path, f"{file_name}.png"), color
        )

        if size is not None:
            colored_image = colored_image.resize(size)

        self.images[name] = ImageTk.PhotoImage(self.__scale_image(colored_image, scale))

    def load_images(self):
        self.images["empty"] = PhotoImage(width=1, height=1)

        if getattr(sys, "frozen", False):
            assert False, "Still needs to be implemented"
        else:
            self.__load_image("stop", "stop_img")
            self.__load_image("skip", "skip_img")
            self.__load_image("pause", "pause_img")
            self.__load_image("play", "play_img")
            self.__load_image("plus", "plus_img")
            self.__load_image("minus", "minus_img")
            self.__load_image("gear", "settings_img")
            self.__load_image("back", "back_img")
            self.__load_image("delete", "delete_img")
            self.__load_image("check_on", "check_on", size=(32, 32))
            self.__load_image("check_off", "check_off", size=(32, 32))
            self.__load_image("eyedropper")
            self.__load_image("eyedropper_inverse", "eyedropper", inverse=True)
            self.__load_image("label")
            self.__load_image("list", "list_img")
            self.__load_image("tag")
            self.__load_image("folder_managed")
            self.__load_image("play_small", "play_img", size=(24, 24))
            self.__load_image("stop_small", "stop_img", size=(24, 24))
