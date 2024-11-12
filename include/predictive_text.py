#!/bin/python3

import tkinter as tk


class PredictiveText(tk.Text):
    def __init__(self, master=None, possible_tags=[], tag_denominator="#", **kw):
        self.popup_background = kw.pop("popup_background", None)

        super().__init__(master, kw)
        super().bind("<Return>", self.__return_add_tag_denominator)
        super().bind("<KeyRelease>", self.__predict)
        super().bind("<FocusOut>", self.__focus_out, add="+")

        self.master = master

        self.possible_tags = possible_tags
        self.added_tags = []
        self.tag_denominator = tag_denominator

        super().insert("0.0", tag_denominator)

        self.predict_popup = None
        self.predict_label = None

        self.last_guess = ""


    def get_added_tags(self):
        return self.added_tags
    

    def get_tags(self):
        text = super().get("1.0", "end-1c")

        if len(text) == 0:
            super().insert("1.0", self.tag_denominator)
            text = super().get("1.0", "end-1c")
            
        char_index_list = self.__get_all_char_pos()

        tags = [text[int(char_index_list[i][0])+1:int(char_index_list[i+1][0])] for i in range(len(char_index_list)-1)]
        tags+= [text[int(char_index_list[-1][0])+1:]]
        
        tags = [tags[i].strip() for i in range(len(tags))]
        tags = [tag for tag in tags if tag != ""]

        return tags


    def update_possible_tags(self, new_possible_tags):
        self.possible_tags = new_possible_tags
    

    def __return_add_tag_denominator(self, key):
        t = super().get("1.0", "end-1c")
        if int(super().index(tk.INSERT).split(".")[1]) != len(t):
            return "break"

        all_tags = self.__get_all_char_pos()
        new_theme = self.__get_new_theme_in_last_position(all_tags)

        if new_theme == "":
            return "break"

        all_tags_text = self.__get_tags(all_tags)
        self.__add_new_tags(all_tags_text)

        prev_index, _ = self.__get_closest_char(all_tags, super().index(tk.INSERT))
       
        super().delete("1."+str(prev_index), tk.END)
        
        super().insert("1."+str(prev_index), self.tag_denominator)
        super().insert("1."+str(prev_index + 1), new_theme)
        super().insert("1."+str(prev_index + 1 + len(new_theme)), " " + self.tag_denominator)

        self.last_guess = ""
        self.__show_popup()

        return "break"
    

    def __get_new_theme_in_last_position(self, char_index_list):
        text = super().get("1.0", "end-1c")
        i = char_index_list[-1][0]
        return text[i+1:]


    def __focus_out(self, _):
        if self.predict_popup != None:
            self.predict_popup.destroy()
            self.predict_popup = None

            self.predict_label.destroy()
            self.predict_label = None


    def __guess_theme(self, word:str) -> str:
        best_guess = ""
        best_score = 0

        for tag in self.possible_tags:
            score = 0

            for char in word:
                if char in tag.lower():
                    score += 1

            THEME_STARTS_WITH_WORD = word == tag.lower()[:len(word)]
            THEME_CONTAINS_WORD = word in tag.lower()

            if THEME_CONTAINS_WORD:
                score = 100 - len(tag)

            if THEME_STARTS_WITH_WORD:
                score = 200 - len(tag)


            if score > best_score:
                best_score = score
                best_guess = tag

        return best_guess

    def __get_all_char_pos(self):
        char_index_list = []
        x, y = 0,1
        for i, c in enumerate(super().get("1.0", "end-1c")):
            if c == self.tag_denominator:
                char_index_list.append((i, str(y) + "." + str(x)))
                x += 1

            elif c == "\n":
                x = 0
                y += 1

            else:
                x += 1

        return char_index_list
    

    def __predict(self, key):
        t = super().get("1.0", "end-1c")

        all_tags = self.__get_all_char_pos()
        all_tags_text = self.__get_tags(all_tags)
        self.__add_new_tags(all_tags_text)

        prev_index, next_index = self.__get_closest_char(all_tags, super().index(tk.INSERT))

        if key.keysym == "Tab" and self.last_guess != "":
            if next_index == -1:
                super().delete("1."+str(prev_index), tk.END)
            else:
                super().delete("1."+str(prev_index), "1."+str(next_index))

            super().insert("1."+str(prev_index), self.tag_denominator)
            super().insert("1."+str(prev_index + 1), self.last_guess)
            super().insert("1."+str(prev_index + 1 + len(self.last_guess)), " " + self.tag_denominator)

            self.last_guess = ""

        else:
            if next_index == -1:
                to_predict = t[prev_index:len(t)]
            else:
                to_predict = t[prev_index:next_index]

            self.last_guess = self.__guess_theme(to_predict.lower()[1:])

        self.__show_popup()


    def __get_tags(self, char_index_list):
        text = super().get("1.0", "end-1c")
        return [text[int(char_index_list[i][0])+1:int(char_index_list[i+1][0])] for i in range(len(char_index_list)-1)]


    def __add_new_tags(self, possible_new):
        for pn in possible_new:
            pn_stripped = pn.strip()

            if pn_stripped not in self.possible_tags:
                self.possible_tags.append(pn_stripped)
                self.added_tags.append(pn_stripped)


    def __get_closest_char(self, list, pos):
        y,x = pos.split(".")
        last = 0
        for i, char in list:
            if int(char.split(".")[0]) < int(y):
                last = i
            elif int(char.split(".")[0]) == int(y):
                if int(char.split(".")[1]) < int(x):
                    last = i
                else:
                    return [last, i]
            else:
                return [last, i]
        return [last, -1]


    def __show_popup(self):
        # Get the current position of the text cursor
        cursor_index = super().index(tk.INSERT)
        bbox = super().bbox(cursor_index)

        if bbox:
            # Get the bounding box of the text cursor
            x, y, _, _ = bbox

            # Get the absolute position of the text widget
            abs_x = super().winfo_rootx() + x + 10
            abs_y = super().winfo_rooty() + y

            if self.predict_popup is None:
                # Create a popup window
                self.predict_popup = tk.Toplevel(self.master)
                self.predict_popup.geometry(f"+{abs_x}+{abs_y}")
                self.predict_popup.wm_overrideredirect(True)

                # Add content to the popup
                self.predict_label = tk.Label(self.predict_popup, text=str(self.last_guess), padx=5, pady=5, background=self.popup_background)
                self.predict_label.pack()

            else:
                self.predict_popup.geometry(f"+{abs_x}+{abs_y}")
                self.predict_label.config(text=str(self.last_guess))


    def destroy(self):
        if self.predict_popup != None:
            self.predict_popup.destroy()
            self.predict_label.destroy()
        super().destroy()


"""
def pr_added(event):
    print(event.widget.get_added_tags())

# --- Constants --- #
APP_NAME = "RPG Music Tool v06_prediction"
START_SIZE = "800x800"
THEMES = ['Festive', 'Large', 'Tavern', 'Open', 'Combat', 'Tense', 'Calm', 'Mysterious', 'Epic', 'War', 'Hopeful', 'Hope', 'Dark', 'Quick', 'Sad', 'Sand', 'Boss', 'Bold']


if __name__ == "__main__":
    root = tk.Tk()

    root.title(APP_NAME)
    root.geometry(START_SIZE)

    text = PredictiveText(root, THEMES, "#", wrap=tk.WORD, width=50, height=20, popup_background="#91a3c4")
    text.bind("<FocusOut>", pr_added)
    text.pack()


    root.mainloop()
"""
