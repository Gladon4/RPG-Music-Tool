import webbrowser
from tkinter import Button, Label, Tk

import requests
import sys
import os


class Updater:
    def __init__(self) -> None:
        self.terminate = False
        self.local_version = self.get_local_version()
        self.online_version = self.get_online_version()

    def get_local_version(self) -> list:
        if getattr(sys, "frozen", False):
            version_path = os.path.join(sys._MEIPASS, "resources/VERSION")
        else:
            version_path = "./resources/VERSION"

        with open(version_path, "r") as v:
            local_verion = v.readline().strip().split(".")

        local_verion = list(map(int, local_verion))

        return local_verion

    def get_online_version(self) -> list:
        try:
            online_version = (
                requests.get(
                    "https://raw.githubusercontent.com/Gladon4/RPG-Music-Tool/refs/heads/main/VERSION"
                )
                .content.decode()
                .strip()
            )

            online_version = online_version.split(".")
            online_version = list(map(int, online_version))

            return online_version

        except requests.exceptions.ConnectionError:
            return self.get_local_version()

    def is_up_to_date(self) -> bool:
        return self.local_version >= self.online_version

    def __version_to_string(self, version: list[int]) -> str:
        return ".".join(list(map(str, version)))

    def remind_user(self):
        self.root = Tk()
        self.root.title(f"Update {self.__version_to_string(self.online_version)} found")
        self.root.geometry("400x200")

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        text = Label(
            self.root,
            text=f"Update {self.__version_to_string(self.online_version)} found!",
            font=("Helvetica", 24),
        )
        text.grid(row=0, column=0, pady=5)

        web_button = Button(
            self.root,
            text="To the Download!",
            command=lambda url="https://www.github.com/Gladon4/RPG-Music-Tool": webbrowser.open(
                url
            ),
            width=20,
        )
        web_button.grid(row=1, column=0, pady=5)

        remind_later = Button(
            self.root,
            text="Remind me again next time",
            command=self.root.destroy,
            width=20,
        )
        remind_later.grid(row=2, column=0, pady=5)

        close_app = Button(self.root, text="Exit", command=self.__terminate, width=20)
        close_app.grid(row=3, column=0, pady=5)

        self.root.mainloop()

    def __terminate(self):
        self.terminate = True
        self.root.destroy()
