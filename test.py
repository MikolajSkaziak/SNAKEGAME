
from tkinter import *
import random
import tkinter as tk

GAME_WIDTH=700
GAME_HEIGHT=700 
MENU_WIDTH=350
MENU_HEIGHT=600
GAME_SPEED=80
SPACE_SIZE=35
SNAKE_PARTS=3
SNAKE_COLOUR="blue"
FOOD_COLOUR="red"
BACKGROUND_COLOUR="black"
colour1='#020f12'
colour2='#05d7ff'
colour3='#65e7ff'
colour4='BLACK'
def on_button_click():
    start_game()
  
    
def start_game():
    main_frame.pack_forget()
    canvas.pack()
    snake = Snake()
    food = Food()
    next_move(snake, food)
    window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")
    
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+{x}+{y}") 
    label.pack() 

# Klasy:
class Snake:
    def __init__(self):
        self.body_size=SNAKE_PARTS
        self.coordinates=[]
        self.squares=[]
        
        for i in range(0,SNAKE_PARTS):
            self.coordinates.append([0, 0])
            
        for x,y in self.coordinates:
             square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE, fill=SNAKE_COLOUR, tag='snake')
             self.squares.append(square)
class Food:
    
    def __init__(self):
        
       x= random.randint(0,int(GAME_WIDTH / SPACE_SIZE)-1)*SPACE_SIZE 
       y= random.randint(0,int(GAME_HEIGHT / SPACE_SIZE)-1)*SPACE_SIZE
       self.coordinates=[x,y]
       canvas.create_oval(x,y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOUR, tag= 'food')



def next_move(snake,food):
  x,y =snake.coordinates[0]
  
  if direction=="up":
      y-=SPACE_SIZE
  elif direction=="down":
      y+=SPACE_SIZE
  elif direction=="left":
      x-=SPACE_SIZE
  elif direction=="right":    
      x+=SPACE_SIZE
   
  snake.coordinates.insert(0,(x,y))  
  square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOUR)  
  snake.squares.insert(0,square)
  if x==food.coordinates[0] and y==food.coordinates[1]:
      global score
      score+=1      
      label.config(text="Score:{}".format(score))
      canvas.delete("food")
      food=Food()
  else:
     del snake.coordinates[-1]
     canvas.delete(snake.squares[-1])
     del snake.squares[-1]
  if check_collision(snake):
     gameover()
  else:
      window.after(GAME_SPEED,next_move,snake,food)    
  

def change_direction(new_direction):
    global direction
    
    if new_direction=='left':
        if direction!='right':
            direction =new_direction 
            
    elif new_direction=='right':
        if direction!='left':
            direction =new_direction
            
    elif new_direction=='up':
        if direction!='down':
            direction =new_direction
            
    elif new_direction=='down':
        if direction!='up':
            direction =new_direction
       

def check_collision(snake):
    
    x,y=snake.coordinates[0]
    
    if x<0 or x>= GAME_WIDTH:
        return True 
    
    elif y<0 or y>=GAME_HEIGHT:
        return True     
    for body_part in snake.coordinates[1:]:
        if x==body_part[0] and y== body_part[1]:
            return True
    return False
def gameover():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,font=('ARIAL',70),text="GAME OVER",fill="red",tag="gameover")
 
#Dostosowanie Okna
window=tk.Tk()
window.title("Snake Game")
window.geometry(f"{MENU_WIDTH}x{MENU_HEIGHT}")
window.resizable(False, False)
score=0
direction='down'
label= Label(window,text="Score:{}".format(score), font=('ARIAL',40))
label.pack()
window.update()
window_width=window.winfo_width()
window_height=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()

x=int((screen_width/2)-(window_width/2))
y=int((screen_height/2)-(window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

main_frame=tk.Frame(window,bg=colour1,pady=40)
main_frame.pack(fill=tk.BOTH,expand=True)
main_frame.columnconfigure(0,weight=1)
main_frame.rowconfigure(0,weight=1)
main_frame.rowconfigure(1,weight=1)

Play_button=tk.Button(
    main_frame,
    background=colour2,
    foreground=colour4,
    activebackground=colour3,
    activeforeground=colour4,
    highlightthickness=2,
    highlightbackground=colour3,
    highlightcolor='WHITE',
    width=13,
    height=2,
    border=0,
    cursor='hand1',
    text='Play',
    font=('ARIAL',20),
    command=on_button_click
    )


Quit_button=tk.Button(
    main_frame,
    background='RED',
    foreground=colour4,
    activebackground=colour3,
    activeforeground=colour4,
    highlightthickness=2,
    highlightbackground=colour3,
    highlightcolor='WHITE',
    width=13,
    height=2,
    border=0,
    cursor='hand1',
    text='Quit',
    font=('ARIAL',20),
    command=window.quit
    )

Settings_button=tk.Button(
    main_frame,
    background=colour2,
    foreground=colour4,
    activebackground=colour3,
    activeforeground=colour4,
    highlightthickness=2,
    highlightbackground=colour3,
    highlightcolor='WHITE',
    width=13,
    height=2,
    border=0,
    cursor='hand1',
    text='Settings',
    font=('ARIAL',20),
    command=on_button_click
    )
Play_button.grid(column=0,row=0)
Settings_button.grid(column=0,row=1)
Quit_button.grid(column=0,row=2)

canvas= Canvas(window,bg=BACKGROUND_COLOUR,height=GAME_HEIGHT,width=GAME_WIDTH)

 
#Przypisanie klawiszy:
window.bind('<Left>',lambda event: change_direction('left'))
window.bind('<Right>',lambda event: change_direction('right'))
window.bind('<Down>',lambda event: change_direction('down'))
window.bind('<Up>',lambda event: change_direction('up'))

window.mainloop()