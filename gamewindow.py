windowSize = [400, 400]

def set_game_window(root):
    width = windowSize[0]
    height = windowSize[1]
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f'{width}x{height}+{x}+{y}')
