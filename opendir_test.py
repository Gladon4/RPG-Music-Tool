from tkinter import *
import tkfilebrowser


APP_NAME = "RPG Music Tool v06_dev"
START_SIZE = "400x400"


root = Tk()
root.title(APP_NAME)
root.geometry(START_SIZE)


def picker():
	dirs = tkfilebrowser.askopendirnames(title="Select your Music Directories", initialdir="/home/", okbuttontext="Select")
	for dir in dirs:
		print(dir)

b = Button(root, text="Test", command=picker)
b.pack()



root.mainloop()