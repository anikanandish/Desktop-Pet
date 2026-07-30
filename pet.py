## Project: Desktop Pet Companion v1.1
# Date: July 21 2026
# TODO: Implement green apple sprite animation

import os
import random
import tkinter as tk
from PIL import Image, ImageTk


class DesktopPet:

    def __init__(self, root, pet_type="default"):
        self.root = root

        # 0. Set pet type FIRST so other variables can check it!
        self.pet_type = pet_type

        # 1. Window Configuration
        self.root.title("My Desktop Pet")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.happiness = 100  # Starts at max happiness

        # 2. Select frames based on pet_type
        if self.pet_type == "green_apple":
            self.frame_files = ["green1.png"]
        else:
            self.frame_files = ["pet1.png", "pet2.png", "pet3.png"]

        # Screen dimensions
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()

        # Core positioning variables
        self.x_pos = 350
        self.y_pos = 350
        self.target_x = self.x_pos
        self.target_y = self.y_pos
        self.root.geometry(f"100x100+{self.x_pos}+{self.y_pos}")
        self.speed = 5  # Pixels it moves per frame update
        self.direction = "right"  # Can be "left" or "right"

        # Load Animation Frames
        self.frames = self.load_frames()
        self.frame_index = 0

        # 3. Setup UI Widget
        self.label = tk.Label(self.root, image=self.frames[0], bg="white")
        self.label.pack()

        # 4. Bind Events
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<ButtonRelease-1>", self.try_to_speak)
        self.label.bind(
            "<Button-3>", lambda e: self.root.destroy()
        )  # Right-click close

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
        if random.random() < 0.70:
            self.target_x = random.randint(0, self.sw - 150)
            self.target_y = random.randint(0, self.sh - 150)

        self.root.after(random.randint(3000, 6000), self.choose_new_action)

    def smooth_move_loop(self):
        """Moves the pet step-by-step to its target with a delay to prevent gliding."""
        dx = self.target_x - self.x_pos
        dy = self.target_y - self.y_pos

        if abs(dx) > self.speed or abs(dy) > self.speed:
            step_x = self.speed if dx > 0 else (-self.speed if dx < 0 else 0)
            step_y = self.speed if dy > 0 else (-self.speed if dy < 0 else 0)

            self.x_pos += step_x
            self.y_pos += step_y
            self.root.geometry(f"+{self.x_pos}+{self.y_pos}")

        self.root.after(500, self.smooth_move_loop)

    def try_to_speak(self, event):
        """Spawns a separate text window right above the pet to avoid visual glitches."""
        self.hide_speech()

        phrases = [
            "Hi Anika!",
            "Keep coding!",
            "Heads up Love",
            "Doing great!",
            "Focus up!",
            "Lets not forget why we're here!",
        ]
        chosen = random.choice(phrases)

        self.speech_window = tk.Toplevel(self.root)
        self.speech_window.overrideredirect(True)
        self.speech_window.wm_attributes("-topmost", True)

        lbl = tk.Label(
            self.speech_window,
            text=chosen,
            bg="#6FC2EF",
            fg="black",
            font=("Arial", 9, "bold"),
            bd=1,
            relief="solid",
            padx=5,
            pady=2,
        )
        lbl.pack()

        bubble_x = self.x_pos + 10
        bubble_y = self.y_pos - 30
        self.speech_window.geometry(f"+{bubble_x}+{bubble_y}")

        self.root.after(2000, self.hide_speech)

    def hide_speech(self):
        """Safely destroys the speech window if active."""
        if self.speech_window:
            self.speech_window.destroy()
            self.speech_window = None


if __name__ == "__main__":
    root = tk.Tk()
    # Pass "green_apple" if you want the green apple pet, or leave blank for default!
    app = DesktopPet(root, pet_type="default")
    root.mainloop()