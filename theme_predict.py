from tkinter import *


# --- Constants --- #
APP_NAME = "RPG Music Tool v06_prediction"
START_SIZE = "800x800"

root = Tk()

root.title(APP_NAME)
root.geometry(START_SIZE)


themes = ['Festive', 'Large', 'Tavern', 'Open', 'Combat', 'Tense', 'Calm', 'Mysterious', 'Epic', 'War', 'Hopeful', 'Hope', 'Dark', 'Quick', 'Sad', 'Sand', 'Boss', 'Bold']


def guess_theme(word:str) -> str:
    best_guess = ""
    best_score = 0

    for theme in themes:
        score = 0

        for char in word:
            if char in theme.lower():
                score += 1


        THEME_STARTS_WITH_WORD = word == theme.lower()[:len(word)]
        THEME_CONTAINS_WORD = word in theme.lower()

        if THEME_CONTAINS_WORD:
            score = 100 - len(theme)
        
        if THEME_STARTS_WITH_WORD:
            score = 200 - len(theme)
            

        if score > best_score:
            best_score = score
            best_guess = theme

        
    return best_guess


def get_all_char_pos(text, char):
    char_index_list = []
    x, y = 0,1
    for i, c in enumerate(text):
        if c == char:
            char_index_list.append((i, str(y) + "." + str(x)))
            x += 1

        elif c == "\n":
            x = 0
            y += 1

        else:
            x += 1
    
    return char_index_list

def get_closest_char(list, pos):
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


        

last_guess_length = 0
last_guess = ""

def predict(key):
    global last_guess_length
    global last_guess

    y,x = text.index(INSERT).split(".")
    t = text.get("1.0", "end-1c")


    all_tags = get_all_char_pos(t, "#")
    prev_index, next_index = get_closest_char(all_tags, text.index(INSERT))

    if next_index == -1:
        prev = t[:prev_index]
        t = t[prev_index:len(t)-last_guess_length]
        after = ""
    else:
        prev = t[:prev_index]
        after = t[next_index:len(t)-last_guess_length]
        t=t[prev_index:next_index]

    if next_index == -1:
        text.delete('0.0', END)

        if key.keysym == "Tab" and last_guess != "":
            text.insert('1.0', prev)
            text.insert('end', "#")
            text.insert('end', last_guess)
            text.insert('end', " #")
            text.insert('end', after)
            
            theme = ""
            last_guess = ""
            last_guess_length = 0
        else:
            theme = " " + guess_theme(t.lower()[1:])
            last_guess = theme[1:]
            last_guess_length = len(theme)

            text.insert('1.0', prev)
            text.insert('end', t)
            text.insert('end', theme, 'guess')
            text.insert('end', after)

            text.mark_set("insert", "%d.%d" % (int(y), int(x)))

    else:
        text.delete('0.0', END)
        text.insert('1.0', prev)
        text.insert('end', t)
        text.insert('end', after)
        last_guess_length = 0
        last_guess = ""
        theme = ""
        text.mark_set("insert", "%d.%d" % (int(y), int(x)))


text = Text(root)
text.insert("0.0", "#")
text.tag_configure("guess", foreground="gray")
text.bind("<KeyRelease>", predict)


text.pack()


root.mainloop()