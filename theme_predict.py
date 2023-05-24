from functools import lru_cache

from tkinter import *


# --- Constants --- #
APP_NAME = "RPG Music Tool v06_dev"
START_SIZE = "800x800"

root = Tk()

root.title(APP_NAME)
root.geometry(START_SIZE)


themes = ['Festive', 'Large', 'Tavern', 'Open', 'Combat', 'Tense', 'Calm', 'Mysterious', 'Epic', 'War', 'Hopeful', 'Hope', 'Dark', 'Quick', 'Sad', 'Sand', 'Boss', 'Bold']

n = [0]

@lru_cache(None)
def editdist(w,v) :
    n[0] = n[0] + 1
    if len(w) == 0 :
        return len(v)
    elif len(v) == 0 :
        return len(w)
    else :
        ed1 = editdist(w,v[:len(v)-1]) + 1               # INS
        ed2 = editdist(w[:len(w)-1],v) + 1               # DEL
        if w[len(w) - 1] == v[len(v) - 1] :
            ed3 = editdist(w[:len(w)-1],v[len(v)-1])     # Nix
        else :
            ed3 = editdist(w[:len(w)-1],v[len(v)-1]) + 1 # REP
        return min(ed1,ed2,ed3)


def guess_theme(word):
    min_dist = 10000
    min_dist_word = ""

    for t in themes:
        n = [0]
        theme_start = t[:len(word)].lower()
        if theme_start != word:
            dist = editdist(word, theme_start)

            if min_dist > dist:
                min_dist_word = t
                min_dist = dist

        else:
            min_dist = 0
            min_dist_word = t

    return min_dist_word

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

    # print(key)

    y,x = text.index(INSERT).split(".")
    t = text.get("1.0", "end-1c")


    all_tags = get_all_char_pos(t, "#")
    prev_index, next_index = get_closest_char(all_tags, text.index(INSERT))

    # print(prev_index, next_index)

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

            # text.mark_set("insert", "%d.%d" % (int(y), int(x)))
            
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

'''
while True:
    word = input("Word please:")
    min_dist = 10000
    min_dist_word = ""

    for t in themes:
        n = [0]
        theme_start = t[:len(word)]
        if theme_start != word:
            dist = editdist(word, theme_start)

            if min_dist > dist:
                min_dist_word = t
                min_dist = dist

        else:
            min_dist = 0
            min_dist_word = t

    print(min_dist_word)
'''
