import csv, os

class Sound_Manager():
	def __init__(self, set_manager):
		self.set_manager = set_manager
		

	# --- Themes --- #
	def load_themes(self):
		self.themes = {}
		self.songs = {}

		try:
			for path in self.set_manager.music_paths:
				self.songs[path] = {}

				with open(path + "/songs.csv", "r", encoding="utf-8-sig") as csv_file:
					list = csv.reader(csv_file, delimiter='\\', quotechar='|')
					for row in list:
						if not row[0] == '':
							self.songs[path][row[0]] = []

						if len(row) >= 2:
							for theme in row[1].split(";"):
								if not theme == "":
									self.songs[path][row[0]].append(theme)
								
		except:
			pass

		self.check_for_new_files()
		self.create_themes_dict()


	def check_for_new_files(self):
		for path in self.set_manager.music_paths:
			for file in os.listdir(path):
				if not file in self.songs[path] and file.endswith(".mp3"):
					print(f"New Song found: {file}")
					self.songs[path][file] = []

			removed_songs = []
			for song in self.songs[path]:
				if not song in os.listdir(path):
					print(f"Deleted File found: {song}")
					removed_songs.append(song)
			
			for song in removed_songs:
				self.songs[path].pop(song, None)

		self.store_themes()

	
	def create_themes_dict(self):
		for path in self.set_manager.music_paths:
			for song in self.songs[path]:
				for theme in self.songs[path][song]:
					if not theme in self.themes:
						self.themes[theme] = []

					self.themes[theme].append(path+song)


	def store_themes(self):
		try:
			for path in self.set_manager.music_paths:
				rows = []

				for song in self.songs[path]:
					themes = ""
					for theme in self.songs[path][song]:
						themes += theme + ";"

					rows.append([song, themes])


				with open(path + "songs.csv", "w", newline="") as file:
					csvwriter = csv.writer(file, delimiter='\\')
					csvwriter.writerows(rows)

		except:
			pass


	# --- SFX --- #
	def load_sfx(self):
		self.sfxs = {}

		try:
			for path in self.set_manager.sfx_paths:
				self.sfxs[path] = []

				with open(path + "/sfx.csv", "r", encoding="utf-8-sig") as csv_file:
					list = csv.reader(csv_file, delimiter='\\', quotechar='|')
					for row in list:
						if not row[0] == '':
							self.sfxs[path] += [row[0]]
		except:
			pass