#main.py
import tkinter as tk
import time

windowTitle = "Button Press Counter"
windowSize = [400, 400]
buttonText = "Press me"
press_count = 0
FPS = 60  # Frames per second

def on_button_press():
    global press_count
    press_count += 1
    print(f"Button pressed {press_count} times")

def set_game_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f'{width}x{height}+{x}+{y}')

def get_delta_time():
    global last_time
    if 'last_time' not in globals():
        last_time = time.time()
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    return delta_time

def move_square():
    global speed_x, speed_y
    delta_time = get_delta_time()
    canvas.move(square, speed_x * delta_time, speed_y * delta_time)
    pos = canvas.coords(square)
    if pos[0] <= 0 or pos[2] >= windowSize[0]:
        speed_x = -speed_x
    if pos[1] <= 0 or pos[3] >= windowSize[1]:
        speed_y = -speed_y

def update():
    move_square()
    root.after(int(1000 / FPS), update)

root = tk.Tk()
root.title(windowTitle)

set_game_window(root, windowSize[0], windowSize[1])

canvas = tk.Canvas(root, width=windowSize[0], height=windowSize[1])
canvas.pack()

square_size = 20
start_x = windowSize[0] / 2 - square_size / 2
start_y = windowSize[1] / 3 - square_size / 2

square = canvas.create_rectangle(start_x, start_y, start_x + square_size, start_y + square_size, fill="blue")

speed_x = 80
speed_y = 80

root.after(int(1000 / FPS), update)  # Start the update loop

button = tk.Button(root, text=buttonText, command=on_button_press)
button.pack()

root.mainloop()
