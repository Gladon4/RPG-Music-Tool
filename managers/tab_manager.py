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
		self.notebook.select(sel.frame)

	def update_all_tab_elements(self):
		for tab in self.tabs:
			self.tabs[tab].update_elements()
