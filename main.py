from sys import exit

from include.app import App
from include.updater import Updater

VERSION = "0.6.0"
APP_NAME = f"RPG Music Tool v{VERSION}"
# This size doesn't really get respected under linux
START_SIZE = "1000x1000"

if __name__ == "__main__":
    updater = Updater()

    if not updater.is_up_to_date():
        updater.remind_user()

    if updater.terminate:
        exit()

    app = App(APP_NAME, START_SIZE)
    app.run()
