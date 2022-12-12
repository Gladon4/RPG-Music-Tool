import csv

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

						if not len(row) < 2:
							for theme in row[1].split(";"):
								if not theme == "":
									self.songs[path][row[0]].append(theme)

									if theme in self.themes:
										self.themes[theme].append(path + row[0])
									else:
										self.themes[theme] = [path + row[0]]
		except:
			pass


	def store_themes(self):
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