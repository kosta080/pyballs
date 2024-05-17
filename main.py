import tkinter as tk
from gamewindow import set_game_window
from game import Game

def main():
    root = tk.Tk()
    set_game_window(root)

    game = Game(root)
    game.setup()
    root.mainloop()

if __name__ == "__main__":
    main()

