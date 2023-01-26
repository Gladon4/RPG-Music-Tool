from tkinter import *
import tkfilebrowser
from managers.settings_manager import Set_Manager


APP_NAME = "OpenDir Test"
START_SIZE = "500x800"


root = Tk()
root.title(APP_NAME)
root.geometry(START_SIZE)


def picker():
	dirs = tkfilebrowser.askopendirnames(title="Select your Music Directories", initialdir="/home/", okbuttontext="Select")
	for dir in dirs:
		print(dir)

def delete(index):
	global paths

	paths[index][0].destroy()
	paths[index][1].destroy()
	del (paths[index])
	set_manager.music_paths = set_manager.music_paths[:index] + set_manager.music_paths[index+1:]

	#print(set_manager.music_paths)
	#print("")
	new_paths = {}
	for i, p in enumerate(paths):
		new_paths[i] = paths[p]
		new_paths[i][0].config(command=lambda i=i: delete(i))
	paths = new_paths


b = Button(root, text="Add", command=picker)
b.pack()

set_manager = Set_Manager()
set_manager.load_paths()

paths = {}

frame = Frame(root)
frame.pack()

paths_text = ""
for i, path in enumerate(set_manager.music_paths):
	path_delete_button = Button(frame, text="del", command=lambda i=i: delete(i))
	path_delete_button.grid(row=i, column=0)
	path_label = Label(frame, text=path,font=("Helvetica",12))
	path_label.grid(row=i, column=1)
	paths[i] = [path_delete_button, path_label]


save_button = Button(root, text="Save", command=set_manager.store_paths)
save_button.pack()


root.mainloop()