from tkinter import *
import pandas as pd
import random
import os.path

known_words = {}
shown_card = {}
words_df={}
words_dict={}
BACKGROUND_COLOR = "#B1DDC6"
current_word = ""

# ---------------------READ KNOWN WORDS---------------------------------#
file_exists = os.path.exists('data/known_words.csv')
if file_exists == FALSE:
    known_words = pd.DataFrame(columns=['English', 'Turkish'])
    known_words = known_words.append({'English' : 'I', 'Turkish' : 'Ben'},
                    ignore_index = True)
    known_words.to_csv('data/known_words.csv', index=False, header=True)
else:
    known_words = pd.read_csv('data/known_words.csv')

# ---------------------READ TO LEARN WORDS---------------------------------#
def read_words():
    global words_df, words_dict
    words_df = pd.read_csv("data/tr_en_words.csv")

    #print(words_df.columns)
    words_df = words_df[~words_df.English.isin(list(known_words.English))]
    words_df =words_df[:11]
    print(len(words_df))
    words_dict = pd.DataFrame.to_dict(words_df,orient="records")

read_words()

def save_word():
    global current_card
    global known_words
    global words_df,words_dict
 #   print(current_card)
    known_words = known_words.append(current_card, ignore_index=True)
    known_words.to_csv('data/known_words.csv', index=False, header=True)
    words_df = words_df[~words_df.English.isin(list(known_words.English))]
    words_dict = pd.DataFrame.to_dict(words_df, orient="records")
    if len(words_dict) <= 1:
        read_words()
    print(len(words_dict))
    canvas.itemconfig(word_left,text=f"{len(words_dict)-1}/10")
    next_card()

# ---------------------SHOW RANDOM WORD---------------------------------#
def next_card():
    global current_card, flip_timer, words_dict, shown_card
    window.after_cancel(flip_timer)
    if len(words_dict) >1:
        current_card = random.choice(words_dict)
        print(shown_card)
        print(current_card)
        while shown_card == current_card:
          #  print("changing")
            current_card = random.choice(words_dict)
    shown_card = current_card
  #  print(current_card["English"])
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_bg, image = card_front_img)
    flip_timer = window.after(3000, func=flip_card)



def flip_card():
    canvas.itemconfig(card_title, text="Turkish", fill="white")
    canvas.itemconfig(card_word, text=current_card["Turkish"], fill="white")
    canvas.itemconfig(card_bg, image = card_bg_image)

# ---------------------CREATE UI---------------------------------#
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_bg_image = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
word_left = canvas.create_text(400, 400, text=f"{len(words_dict)-1}/10", font=("Ariel", 30, "italic"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)



wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0,command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0,command=save_word)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
