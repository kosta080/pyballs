import tkinter as tk
import time
import math
from calc import Calc
class Game:
    FPS = 120

    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.last_time = time.time()
        self.speed_x = 80  # Speed of the square in pixels per second
        self.speed_y = 80

    def setup(self):
        # Calculate the center of the canvas
        center_x = self.canvas.winfo_width() / 2
        center_y = self.canvas.winfo_height() / 2

        self.line = self.canvas.create_line(0, 300, 200, 10, fill="red")

        # Create a ball
        self.ball = self.canvas.create_oval(200, 200, 250, 250, fill="blue")
        self.ball_velocity = [1.222, 1.222]  # Initial velocity of the ball

        # Create text items
        self.text_closest_point = self.canvas.create_text(10, 380, anchor="w", fill="black", font="Arial 10")
        self.text_distance = self.canvas.create_text(10, 395, anchor="w", fill="black", font="Arial 10")

        # Start the animation
        self.animate()

    def start_drag(self, event):
        # Record the item and its location at the start of dragging
        self.drag_data = {"x": event.x, "y": event.y, "item": self.box}

    def drag(self, event):
        # Calculate how much the mouse has moved
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]

        # Move the object the appropriate amount
        self.canvas.move(self.drag_data["item"], delta_x, delta_y)

        # Record the new position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def stop_drag(self, event):
        # Clear the drag data
        self.drag_data = {}

    
    def animate(self):
        # Move the ball
        self.canvas.move(self.ball, *self.ball_velocity)
        ball_coords = self.canvas.coords(self.ball)
        ball_center_x = (ball_coords[0] + ball_coords[2]) / 2
        ball_center_y = (ball_coords[1] + ball_coords[3]) / 2

        # Get line coordinates
        line_coords = self.canvas.coords(self.line)
        lx1, ly1, lx2, ly2 = line_coords

        # Calculate the closest point on the line to the ball's center
        closest_point = Calc.closest_point_on_line(lx1, ly1, lx2, ly2, ball_center_x, ball_center_y)
        distance_to_closest_point = Calc.distance((ball_center_x, ball_center_y), closest_point)
        if distance_to_closest_point < 25:
            new_vx, new_vy = Calc.reflect_vector(ball_center_x, ball_center_y, self.ball_velocity[0], self.ball_velocity[1], closest_point[0], closest_point[1])
            self.ball_velocity = [new_vx, new_vy]


        # Update text on the canvas
        self.canvas.itemconfig(self.text_closest_point, text=f"Closest point on the line: {closest_point}")
        self.canvas.itemconfig(self.text_distance, text=f"Distance to the closest point: {distance_to_closest_point}")

        # Bounce off the walls
        if ball_coords[0] <= 0 or ball_coords[2] >= self.canvas.winfo_width():
            self.ball_velocity[0] = -self.ball_velocity[0]
        if ball_coords[1] <= 0 or ball_coords[3] >= self.canvas.winfo_height():
            self.ball_velocity[1] = -self.ball_velocity[1]

        self.canvas.after(50, self.animate)  # Schedule next animation frame

    def check_collision(self, ball_coords, box_coords):
        # Convert flat list of box coordinates to a list of (x, y) tuples
        box_coords = [(box_coords[i], box_coords[i+1]) for i in range(0, len(box_coords), 2)]

        ball_left, ball_top, ball_right, ball_bottom = ball_coords
        box_left = min(x for x, y in box_coords)
        box_top = min(y for x, y in box_coords)
        box_right = max(x for x, y in box_coords)
        box_bottom = max(y for x, y in box_coords)

        return not (ball_right < box_left or ball_left > box_right or ball_bottom < box_top or ball_top > box_bottom)



    def handle_collision(self, ball_coords, box_coords):
        # Convert flat list of box coordinates to a list of (x, y) tuples
        box_coords = [(box_coords[i], box_coords[i+1]) for i in range(0, len(box_coords), 2)]

        ball_left, ball_top, ball_right, ball_bottom = ball_coords
        box_left = min(x for x, y in box_coords)
        box_top = min(y for x, y in box_coords)
        box_right = max(x for x, y in box_coords)
        box_bottom = max(y for x, y in box_coords)

        # Check if collision is more likely horizontal or vertical
        overlap_left = ball_right - box_left
        overlap_right = box_right - ball_left
        overlap_top = ball_bottom - box_top
        overlap_bottom = box_bottom - ball_top

        # Find the minimum overlap
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_top:
            self.ball_velocity[1] = -abs(self.ball_velocity[1])  # Ensure the ball moves upward
        elif min_overlap == overlap_bottom:
            self.ball_velocity[1] = abs(self.ball_velocity[1])  # Ensure the ball moves downward
        elif min_overlap == overlap_left:
            self.ball_velocity[0] = -abs(self.ball_velocity[0])  # Ensure the ball moves left
        elif min_overlap == overlap_right:
            self.ball_velocity[0] = abs(self.ball_velocity[0])  # Ensure the ball moves right


    def get_delta_time(self):
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        return delta_time
