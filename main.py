#!/bin/python3

from include.app import App

VERSION = "060_dev"
APP_NAME = f"RPG Music Tool v{VERSION}"
START_SIZE = "800x1000"

if __name__ == "__main__":
    app = App(APP_NAME, START_SIZE)
    app.run()
