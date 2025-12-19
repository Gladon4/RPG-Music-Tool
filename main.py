#!/bin/python3

from tkinter import Tk

from include.app import App
from include.updater import Updater

VERSION = "060_dev"
APP_NAME = f"RPG Music Tool v{VERSION}"
START_SIZE = "800x1000"

if __name__ == "__main__":
    updater = Updater()

    if not updater.is_up_to_date():
        updater.remind_user()

    if updater.terminate:
        exit()

    app = App(APP_NAME, START_SIZE)
    app.run()
