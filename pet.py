import tkinter as tk
from PIL import Image, ImageTk
import os
import random

class DesktopPet:
    def __init__(self, root):
        self.root = root
        # 1. Window Configuration
        self.root.title("My Desktop Pet")
        self.root.overrideredirect(True)
        
        # 1. Window Configuration
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")
        
        # Screen dimensions
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        
        # Core positioning variables
        self.x_pos = 300
        

        self.y_pos = 300
        self.target_x = self.x_pos
        self.target_y = self.y_pos
        self.root.geometry(f"100x100+{self.x_pos}+{self.y_pos}")
        # Track current state
        self.state = "idle"
      




        # 2. Load Animation Frames
        self.frame_files = ["pet1.png", "pet2.png", "pet3.png"]
        self.frames = self.load_frames()
        self.frame_index = 0

        # 3. Setup UI Widget
        self.label = tk.Label(self.root, image=self.frames[0], bg='white')
        self.label.pack()

        # 4. Bind Events
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<Button-3>", lambda e: self.root.destroy()) # Right-click close

        # 5. Start Loops
        self.animate()
        self.choose_new_action()
        self.smooth_move_loop()
    def load_frames(self):
        """Loads and resizes image assets safely!"""
        loaded_frames = []
        for file in self.frame_files:
            if os.path.exists(file):
                img = Image.open(file).resize((100, 100))
                loaded_frames.append(ImageTk.PhotoImage(img))
            else:
                print(f"Error: Missing image file '{file}'")
                self.root.destroy()
                exit()
        return loaded_frames

    def start_drag(self, event):
        """Stores internal click offsets for dragging."""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    def drag(self, event):
        """Handles manual dragging, updating targets so it doesn't snap back."""
        self.x_pos = event.x_root - self.drag_start_x
        self.y_pos = event.y_root - self.drag_start_y
        
        # Sync targets so the pet stays put when dropped
        self.target_x, self.target_y = self.x_pos, self.y_pos
        self.root.geometry(f"+{self.x_pos}+{self.y_pos}")
    def animate(self):
        """Cycles through the loaded sprite frames."""
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.label.config(image=self.frames[self.frame_index])
        self.root.after(350, self.animate)

    def choose_new_action(self):
        """Every few seconds, decides whether to stay still or pick a new target position."""
        # 70% chance to move, 30% chance to sit idle
        if random.random() < 0.70:
            # Pick a completely random spot on the screen
            # Shaving 150 off height keeps it safely above standard taskbars
            self.target_x = random.randint(0, self.sw - 100)
            self.target_y = random.randint(0, self.sh - 150)
        
        # Decide next action interval (between 3 to 6 seconds)
        self.root.after(random.randint(3000, 6000), self.choose_new_action)

    def smooth_move_loop(self):
        """Moves the pet fractions of the way to its target every 20ms for smooth sliding."""
        # Calculate distance to target
        dx = self.target_x - self.x_pos
        dy = self.target_y - self.y_pos

        # If we are far enough from target, step closer (easing effect)
        if abs(dx) > 2 or abs(dy) > 2:
            self.x_pos += int(dx * 0.05) # Moves 5% of the remaining distance per frame
            self.y_pos += int(dy * 0.05)
            self.root.geometry(f"+{self.x_pos}+{self.y_pos}")

        # Run at ~50 FPS for smooth rendering
        self.root.after(20, self.smooth_move_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopPet(root)
    root.mainloop()

