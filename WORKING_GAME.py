# Import necessary libraries
from tkinter import *
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk

# Define constants and configurations for the game
GAME_WIDTH=700
GAME_HEIGHT=700
GAME_SPEED=150  
SPACE_SIZE=35
SNAKE_PARTS=3
SNAKE_COLOUR="GREEN"
SNAKE_COLOUR_HEAD="greenyellow"
FOOD_COLOUR="red"
BACKGROUND_COLOUR="black"

# Define color constants for the UI
colour1='#020f12'
colour2='#05d7ff'
colour3='greenyellow'
colour4='BLACK'

# Define available window resolutions for the game
available_resolutions = ["700x700", "800x800", "900x900","1280x960"]

# Initialize variables for the current resolution and UI elements
current_resolution_index = 0
current_resolution_label = None
menu_background = None 

# Class representing the Snake in the game
class Snake:
    def __init__(self):
        # Initialize attributes for the snake
        self.body_size = SNAKE_PARTS
        self.coordinates = []
        self.squares = []
        # Create initial coordinates for the snake
        for i in range(0, SNAKE_PARTS):
            self.coordinates.append([0, 0])
        # Create rectangles for each part of the snake
        for i, (x, y) in enumerate(self.coordinates):
            fill_color = SNAKE_COLOUR if i == 0 else SNAKE_COLOUR_HEAD
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=fill_color, tag='snake')
            self.squares.append(square)
    # Update the color of the snake's head
    def update_head_color(self):
        if not self.head_colored:
            canvas.itemconfig(self.squares[0], fill=SNAKE_COLOUR_HEAD)
            self.head_colored = True
            
# Class representing the food in the game
class Food:
    
    def __init__(self):
       # Generate random coordinates for the food
       x= random.randint(0,int(width / SPACE_SIZE)-1)*SPACE_SIZE 
       y= random.randint(0,int(height / SPACE_SIZE)-1)*SPACE_SIZE
       self.coordinates=[x,y]
       # Create an oval representing the food
       canvas.create_oval(x,y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOUR, tag= 'food')



        
        
# Function to update the highscore file 
def update_highscore_file():        
        with open("highscore.txt", "w") as file:
            file.write(str(highscore))
            
# Function to read the highscore from the file
def read_highscore_file():
    try:
        with open("highscore.txt", "r") as file:
            content = file.read()
            if content.strip(): 
                return int(content)
            else:
                return 0
    except FileNotFoundError:
        return 0
    
# Initialize highscore and related UI elements    
highscore = read_highscore_file()
highscore_label = None    
       
# Function to start the game
def start_game():
    
    global label, canvas, window, score
    
    score=0
    
    # Hide the main menu frame
    main_frame.pack_forget()
    
     # Create and display the score label
    label= Label(window,text="Score:{}".format(score), font=('ARIAL',40))
    label.pack()
    
    # Create and display the game canvas
    canvas= Canvas(window,bg=BACKGROUND_COLOUR,height=height,width=width)
    canvas.pack()
    
    # Set the window dimensions based on the canvas size    
    window.geometry(f"{width}x{height+75}")
    
    # Initialize the snake and food objects and start the game loop
    snake = Snake()
    food = Food()
    next_move(snake, food)
    
# Function to handle the next move in the game    
def next_move(snake, food):

    x, y = snake.coordinates[0]

    # Update the coordinates based on the current direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
        
    # Update the snake's coordinates and create a new rectangle for the head
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR_HEAD)
    snake.squares.insert(0, square)

    global GAME_SPEED

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
        GAME_SPEED -= 2
        
    else:
        # Update the color of snake parts and remove the last part
        for i in range(len(snake.squares)):
            if i == 0:
                canvas.itemconfig(snake.squares[i], fill=SNAKE_COLOUR_HEAD)
            else:
                canvas.itemconfig(snake.squares[i], fill=SNAKE_COLOUR)

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    # Check for collision with walls or itself
    if check_collision(snake):
        gameover()
        
    else:
        # Continue the game loop with the updated speed
        window.after(GAME_SPEED, next_move, snake, food)
        
# Function to change the direction of the snake based on key presses        
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
       
# Function to check collision with walls or itself
def check_collision(snake):
    
    x,y=snake.coordinates[0]
    
    if x<0 or x>= width:
        return True 
    
    elif y<0 or y>=height:
        return True     
    
    for body_part in snake.coordinates[1:]:
        
        if x==body_part[0] and y== body_part[1]:
            return True
        
    return False

# Function to handle the gameover scenario
def gameover():
    
    global highscore_label, highscore
    
    #Update the window geometry
    window.geometry(f"{width}x{height}")
    
    # Clear the canvas and display the game over message
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
        font=('ARIAL', 70),
        text="GAME OVER",
        fill="red",
        tag="gameover")
    
    # Hide the score label
    label.pack_forget()

    # Display Play Again and Quit buttons
    play_again_button = tk.Button(
        window,
        background='Green',
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour3,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=0,
        cursor='hand2',
        text='Play Again',
        font=('ARIAL', 20),
        command=reset_game
    )
    play_again_button_window = canvas.create_window(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 150,
        anchor='center', window=play_again_button
    )

    quit_button = tk.Button(
        window,
        background='RED',
        foreground=colour4,
        activebackground='lightcoral',
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground='lightcoral',
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=0,
        cursor='hand2',
        text='Quit',
        font=('ARIAL', 20),
        command=window.quit
    )
    quit_button_window = canvas.create_window(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 250,
        anchor='center', window=quit_button
    )
    
    # Update and display the highscore
    global highscore_label,highscore
    
    if score > highscore:
        highscore = score
        update_highscore_file()
        
    highscore = read_highscore_file()
    highscore_label = canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50,
        font=('ARIAL', 20),
        text="Highscore: {}".format(highscore),
        fill="white",
        tag="highscore")
    
# Function to reset the game
def reset_game():
    
    global direction
    # Hide the canvas
    canvas.pack_forget()
    # Reset score and direction
    score = 0
    direction = 'down'
    
    # Destroy existing UI buttons
    for widget in window.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()
            
    # Update and display the score label
    label.config(text="Score:{}".format(score))
    # Start the game again 
    start_game()
    

# Function to display the game settings    
def settings():
    
    global settings_frame, current_resolution_label
    
    # Hide the main menu frame
    main_frame.pack_forget()
    
    # Create the settings frame
    settings_frame = tk.Frame(window, bg=colour1, pady=40)
    settings_frame.pack(fill=tk.BOTH, expand=True)
    settings_frame.columnconfigure(0, weight=1)
    settings_frame.rowconfigure(0, weight=1)
    settings_frame.rowconfigure(1, weight=1)
    
    # Create Back button to return to the main menu
    back_to_menu = tk.Button(
        settings_frame,
        background='Green',
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour3,
        highlightcolor='WHITE',
        width=13,
        height=1,
        border=0,
        cursor='hand2',
        text='Back',
        font=('ARIAL', 20),
        command=Back_to_menu)
    back_to_menu.pack(side='bottom', anchor=tk.S, pady=(10, 0)
    )
    
    # Create label to display the current window resolution
    current_resolution_label = tk.Label(
        settings_frame,
        text=f"Current Window Resolution: {available_resolutions[current_resolution_index]}",
        font=('ARIAL', int(15 * (width / 700))), 
        bg=colour1,
        fg='white',
    )
    current_resolution_label.pack(pady=(20, 10))
    
    # Create frame for resolution navigation buttons
    resolution_buttons_frame = tk.Frame(settings_frame, bg=colour1)
    resolution_buttons_frame.pack(pady=(10, 0))
    
    # Create buttons to navigate resolutions
    Leftarrow = tk.Button(
        resolution_buttons_frame,
        background='Green',
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour3,
        highlightcolor='WHITE',
        width=5,
        height=1,
        border=0,
        cursor='hand2',
        text='<',
        font=('ARIAL', 20 ), 
        command=lambda: apply_resolution("left")
        )
    Leftarrow.pack(side='left', padx=(10, 5)) 

  
    tk.Label(resolution_buttons_frame, bg=colour1, width=1).pack(side='left')

    Rightarrow = tk.Button(
        resolution_buttons_frame,
        background='Green',
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour3,
        highlightcolor='WHITE',
        width=5,
        height=1,
        border=0,
        cursor='hand2',
        text='>',
        font=('ARIAL', 20 ),
        command=lambda: apply_resolution("right")
        )
    Rightarrow.pack(side='left', padx=(5, 10))  

    # Create space in the settings frame
    tk.Label(settings_frame, bg=colour1, height=1).pack()
    
    # Create button to confirm the selected resolution
    confirm_button = tk.Button(
        settings_frame,
        background='Green',
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour3,
        highlightcolor='WHITE',
        width=8,
        height=1,
        border=0,
        cursor='hand2',
        text='Apply',
        font=('ARIAL',20) ,
        command=confirm_resolution
    )
    confirm_button.pack(pady=(0,150))
    
    # Create button to reset the highest score
    reset_highestscore_button = tk.Button(
        settings_frame,
        background='Green',
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour3,
        highlightcolor='WHITE',
        width=17,
        height=1,
        border=0,
        cursor='hand2',
        text='Reset highest score',
        font=('ARIAL',20) ,
        command=reset_highest_score
    )
    reset_highestscore_button.pack(pady=(0,150))
    
# Function to reset highest score
def reset_highest_score():
    response = messagebox.askyesno("Confirmation", "Are you sure you want to reset the highest score?")
    if response:
        with open("highscore.txt", "w") as file:
            pass 
         
# Function to navigate and apply resolutions   
def apply_resolution(direction):
    
    global current_resolution_index, current_resolution_label,height,width
    
    # Navigate to the left or right based on the direction
    if direction == "left":
        current_resolution_index = (current_resolution_index - 1) % len(available_resolutions)
    elif direction == "right":
        current_resolution_index = (current_resolution_index + 1) % len(available_resolutions)

    selected_resolution = available_resolutions[current_resolution_index]
    current_resolution_label.config(text=f"Current Window Resolution: {selected_resolution}")
    
# Function to confirm and apply the selected resolution    
def confirm_resolution():
    
    global height, width
    
    selected_resolution = available_resolutions[current_resolution_index]
    width, height = map(int, selected_resolution.split("x"))
    
    # Set the window geometry and update
    window.geometry(f"{width}x{height}")
    current_resolution_label.config(text=f"Current Window Resolution: {width}x{height}")
    Centering_window()
# Center the window on the screen
def Centering_window():    
    window_width = window.winfo_screenwidth()
    window_height = window.winfo_screenheight()
    screen_width = width
    screen_height = height
    Position_left = int(window_width/2 - screen_width/2)
    Position_Up = int(window_height/2 - screen_height/2)
    if height < 900:
        window.geometry(f"{screen_width}x{screen_height}+{Position_left}+{Position_Up}")
    else: 
        window.geometry(f"{screen_width}x{screen_height}+{Position_left}+{Position_Up-50}")
    window.update()
    
def Back_to_menu():
    # Hide the settings frame to go back to the main menu
    settings_frame.pack_forget()
    # Call the main menu function
    Menu()
    
def Menu():
    
    global main_frame, menu_background
    # Create the main frame for the menu
    main_frame=tk.Frame(window,bg='#96d201',pady=40)
    main_frame.pack(fill=tk.BOTH,expand=True)
    main_frame.columnconfigure(0,weight=1)
    main_frame.rowconfigure(0,weight=1)
    main_frame.rowconfigure(1,weight=1)
    # Load the menu background image
    menu_background=Image.open('MENU_BACKGROUND.jpg')
    menu_background=ImageTk.PhotoImage(menu_background)
    # Display the menu background
    Menu_background = Label(main_frame,bg='#96d201' ,image=menu_background, bd=0)
    Menu_background.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Create buttons for Play, Settings, and Quit
    Play_button=tk.Button(
        main_frame,
        background='Green',
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour3,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=0,
        cursor='hand2',
        text='Play',
        font=('ARIAL',20),
        command=start_game
    )

    Quit_button=tk.Button(
        main_frame,
        background='RED',
        foreground=colour4,
        activebackground='lightcoral',
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour3,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=0,
        cursor='hand2',
        text='Quit',
        font=('ARIAL',20),
        command=window.quit
    )

    Settings_button=tk.Button(
        main_frame,
        background='Green',
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour3,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=0,
        cursor='hand2',
        text='Settings',
        font=('ARIAL',20),
        command=settings
    )
    # Pack the buttons onto the main menu
    Play_button.pack(pady=50,  expand=True)
    Settings_button.pack(pady=50, expand=True)
    Quit_button.pack(pady=50, expand=True)
# Create the main window    
window=tk.Tk()
window.title("Snake Game")
# Set the initial window size and make it non-resizable
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")
window.resizable(False, False)
# Initialize game variables
score=0
direction='down'
height=GAME_HEIGHT
width=GAME_WIDTH
# Update the window to get accurate dimensions
window.update()
# Center the window on the screen
Centering_window()
# Initialize the menu
menu=Menu()

# Set up keybindings for controlling the snake
window.bind('<Left>',lambda event: change_direction('left'))
window.bind('<Right>',lambda event: change_direction('right'))
window.bind('<Down>',lambda event: change_direction('down'))
window.bind('<Up>',lambda event: change_direction('up'))
# Start the Tkinter main loop
window.mainloop()