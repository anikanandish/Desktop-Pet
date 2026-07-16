# Project: Desktop Pet Companion v1.1
# Date: July 2026

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
        self.happiness = 100  # Starts at max happiness
        self.click_count = 0  # Tracks user interactions
        
        # Screen dimensions
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        
        # Core positioning variables
        self.x_pos = 300
        

        self.y_pos = 300
        self.target_x = self.x_pos
        self.target_y = self.y_pos
        self.root.geometry(f"100x100+{self.x_pos}+{self.y_pos}")
        self.speed = 5  # Pixels it moves per frame update
        self.direction = "right"  # Can be "left" or "right"
        self.last_interact_time = 0  # Tracks timestamp of last click
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
        self.label.bind("<ButtonRelease-1>", self.try_to_speak)
        self.label.bind("<Button-3>", lambda e: self.root.destroy()) # Right-click close
        self.is_sleeping = False  # Track if the pet is awake or asleep
        self.speech_window = None  # Tracks the floating speech bubble window

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
        """Moves the pet step-by-step to its target with a delay to prevent gliding."""
        # Calculate distance to target
        dx = self.target_x - self.x_pos
        dy = self.target_y - self.y_pos

        # If we are far enough from target, take one distinct, choppy step
        if abs(dx) > self.speed or abs(dy) > self.speed:
            # Move by your flat speed (5 pixels) instead of a smooth percentage sliding scale
            step_x = self.speed if dx > 0 else (-self.speed if dx < 0 else 0)
            step_y = self.speed if dy > 0 else (-self.speed if dy < 0 else 0)
            
            self.x_pos += step_x
            self.y_pos += step_y
            self.root.geometry(f"+{self.x_pos}+{self.y_pos}")

        # Changed from 20ms to 500ms so it pauses completely between steps!
        self.root.after(500, self.smooth_move_loop)


    def check_blink(self):
        # A simple 10% chance to blink on any given frame update
        import random
        if random.random() < 0.10:
            print("Blinking!") # to be hooked up to a blink frame later
    def update_movement(self):
        # Move right if direction is right, move left if direction is left
        if self.direction == "right":
            self.root.geometry(f"+{self.root.winfo_x() + self.speed}+{self.root.winfo_y()}")
        else:
            self.root.geometry(f"+{self.root.winfo_x() - self.speed}+{self.root.winfo_y()}")
  
    def try_to_speak(self, event):
        """Spawns a separate text window right above the pet to avoid visual glitches."""
        self.hide_speech() # Close any existing bubble first
        
        phrases = [
            "Hi Anika!", 
            "Keep coding!", 
            "Break time?", 
            "Doing great!", 
            "Focus up! "
        ]
        chosen = random.choice(phrases)
        
        # 1. Create a tiny separate window just for the text
        self.speech_window = tk.Toplevel(self.root)
        self.speech_window.overrideredirect(True)
        self.speech_window.wm_attributes("-topmost", True)
        
        # 2. Design the text label inside it
        lbl = tk.Label(
            self.speech_window, 
            text=chosen, 
            bg="#FFFFE0", # Classic light yellow comic bubble color
            fg="black", 
            font=("Arial", 9, "bold"), 
            bd=1, 
            relief="solid", 
            padx=5, 
            pady=2
        )
        lbl.pack()
        
        # 3. Position it centered right above the pet
        bubble_x = self.x_pos + 10
        bubble_y = self.y_pos - 30 
        self.speech_window.geometry(f"+{bubble_x}+{bubble_y}")
        
        # 4. Make it disappear automatically after 2 seconds
        self.root.after(2000, self.hide_speech)

    def hide_speech(self):
        """Safely destroys the speech window if it is currently active."""
        if self.speech_window:
            self.speech_window.destroy()
            self.speech_window = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopPet(root)
    root.mainloop()

