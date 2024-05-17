import tkinter as tk
import time
import math

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

        # Define the size of the hexagon
        size = 50  # Distance from center to each vertex

        # Calculate the vertices of the hexagon
        hexagon_points = [
            (center_x + size * math.cos(math.radians(angle)), center_y + size * math.sin(math.radians(angle)))
            for angle in range(0, 360, 60)  # 0, 60, 120, ..., 300 degrees
        ]

        # Create a hexagon
        self.box = self.canvas.create_polygon(hexagon_points, fill="red", outline="black")

        # Create a ball
        self.ball = self.canvas.create_oval(190, 190, 210, 210, fill="blue")
        self.ball_velocity = [2, 2]  # Initial velocity of the ball

        # Bind mouse events for the hexagon
        self.canvas.tag_bind(self.box, "<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.box, "<B1-Motion>", self.drag)
        self.canvas.tag_bind(self.box, "<ButtonRelease-1>", self.stop_drag)

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

        # Check for collision with the box
        box_coords = self.canvas.coords(self.box)
        if self.check_collision(ball_coords, box_coords):
            self.handle_collision(ball_coords, box_coords)

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
