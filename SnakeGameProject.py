
from tkinter import Label, Tk, Canvas


GAME_WIDTH=700
GAME_HEIGHT=700 
GAME_SPEED=50
SPACE_SIZE=30
SNAKE_PARTS=3
SNAKE_COLOUR="blue"
FOOD_COLOUR="red"
BACKGROUND_COLOUR="black"
# Klasy:

class Snake:
    pass

class Food:
    pass

class Counter:
    pass

# Funkcje:

def next_move():
  pass

def change_direction(new_direction):
    pass

def check_collision():
    pass        

def gameover():
    pass
#Dostosowanie Okna
window = Tk()
window.title("Snake Game")
window.resizable(False, False)
score=0
direction='down'
label= Label(window,text="Score:{}".format(score), font=('consolas',40))
label.pack()
canvas= Canvas(window,bg=BACKGROUND_COLOUR,height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()
window.mainloop()