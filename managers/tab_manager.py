"""
Manages Notebook Tabs
"""

class Tab_Manager():
	def __init__(self, notebook):
		self.notebook = notebook
		self.tabs = {}


	def set_tabs(self, tabs):
		self.tabs = tabs

	def select(self, tab):
		sel = self.tabs[tab]
		self.notebook.select(sel)
