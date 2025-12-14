from tkinter import Button, Frame, LabelFrame, Widget, ttk
from typing import Callable

from managers.image_manager import ImageManager
from managers.settings_manager import SetttingsManager
from managers.tab_manager import TabManager


class Tab:
    def __init__(
        self,
        settings_manager: SetttingsManager,
        tab_manager: TabManager,
        image_manager: ImageManager,
        notebook: ttk.Notebook,
    ) -> None:
        self.settings_manager = settings_manager
        self.tab_manager = tab_manager
        self.image_manager = image_manager
        self.notebook = notebook

        self.widgets: list[Widget] = []

    def create(self, new: bool = False):
        settings = self.settings_manager.settings
        if not new:
            self.frame = Frame(
                self.notebook,
                width=0,
                height=0,
                bg=settings["bg_color"],
            )
            self.frame.grid_rowconfigure(0, weight=0)
            self.frame.grid_columnconfigure(0, weight=1)

        self.navigation_buttons_frame = LabelFrame(
            self.frame, bg=settings["bg_color"], padx=0, borderwidth=0
        )
        self.navigation_buttons_frame.place(relx=1.0, rely=0, anchor="ne")
        self.widgets.append(self.navigation_buttons_frame)

    def add_button(
        self,
        frame: Frame | LabelFrame,
        text: str = "",
        image: str = "empty",
        scale: float = 1,
        command: Callable = lambda _: _,
        wraplength: int = 0,
        font_size: float = 1,
    ) -> Button:
        settings = self.settings_manager.settings
        button = Button(
            frame,
            text=text,
            image=self.image_manager.images[image],
            compound="center",
            borderwidth=0,
            activebackground=settings["button_hov_color"],
            bg=settings["button_bg_color"],
            fg=settings["txt_color"],
            height=int(settings["ui_scale"] * scale),
            width=int(settings["ui_scale"] * scale),
            command=command,
            wraplength=wraplength,
            highlightbackground=settings["button_hov_color"],
            font=("Helvetica", int(settings["font_size"] * font_size)),
        )
        self.widgets.append(button)

        return button

    def add_navigation_button(self, destination: str, image: str):
        navigation_button = self.add_button(
            frame=self.navigation_buttons_frame,
            command=lambda x=self: self.tab_manager.select(destination),
            image=image,
            scale=0.4,
        )
        navigation_button.pack(side="bottom")

    def update(self):
        self.frame.config(bg=self.settings_manager.settings["bg_color"])
        self.destroy()
        self.create()

    def destroy(self):
        for widget in self.widgets:
            widget.destroy()
