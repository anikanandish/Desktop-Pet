import math
from pathlib import Path
import random
import sys
import tkinter as tk
from PIL import Image, ImageTk

SCRIPT_DIR = Path(__file__).resolve().parent


class DesktopPet:

    def __init__(self, root, pet_type="default"):
        self.root = root
        self.pet_type = pet_type

        # Window Configuration
        self.root.title("My Desktop Pet")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")

        # Frame definitions
        if self.pet_type == "green_apple":
            self.frame_files = ["green1.png", "green2.png", "green3.png"]
        elif self.pet_type == "f1":
            self.frame_files = ["f1_1.png", "f1_2.png", "f1_3.png"]
        elif self.pet_type == "lewis":
            self.frame_files = ["lh1.png", "lh2.png", "lh3.png"]
        else:
            self.frame_files = ["pet1.png", "pet2.png", "pet3.png"]

        # Screen boundaries
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()

        # Position and physics state
        self.x_pos = 350.0
        self.y_pos = 350.0
        self.is_dragging = False
        self.root.geometry(f"100x100+{int(self.x_pos)}+{int(self.y_pos)}")

        # F1 style waypoint motion
        self.is_car = self.pet_type in ["f1", "lewis"]
        self.current_speed = 6.0 if self.is_car else 3.0
        self.target_x = self.x_pos
        self.target_y = self.y_pos

        self.frames = self.load_frames()
        self.frame_index = 0

        self.label = tk.Label(self.root, image=self.frames[0], bg="white")
        self.label.pack()

        # Bind events
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)
        self.label.bind("<Button-3>", lambda e: self.root.destroy())

        self.speech_window = None
        self.speech_timer = None

        # Start game loops
        self.animate()
        self.pick_next_track_sector()
        self.smooth_move_loop()

    def load_frames(self):
        loaded = []
        for file in self.frame_files:
            file_path = SCRIPT_DIR / file
            if file_path.exists():
                img = Image.open(file_path).resize((100, 100))
                loaded.append(ImageTk.PhotoImage(img))
            else:
                print(f"Error: Missing image file '{file_path}'")
                self.root.destroy()
                sys.exit(1)
        return loaded

    def start_drag(self, event):
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def drag(self, event):
        self.x_pos = float(event.x_root - self.drag_start_x)
        self.y_pos = float(event.y_root - self.drag_start_y)
        self.target_x, self.target_y = self.x_pos, self.y_pos
        self.root.geometry(f"+{int(self.x_pos)}+{int(self.y_pos)}")
        self.update_speech_position()

    def stop_drag(self, event):
        self.is_dragging = False
        self.try_to_speak()

    def animate(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.label.config(image=self.frames[self.frame_index])
        delay = 140 if self.is_car else 300
        self.root.after(delay, self.animate)

    def pick_next_track_sector(self):
        """Simulates driving circuits (straights + turns) instead of random teleporting."""
        if not self.is_dragging:
            margin = 120
            if self.is_car:
                pattern = random.choice(
                    ["straight_fast", "chicane", "hairpin", "sweep"]
                )

                if pattern == "straight_fast":
                    # Full screen straight blast
                    self.target_x = random.choice([margin, self.sw - margin])
                    self.target_y = self.y_pos + random.choice(
                        [-80, 0, 80]
                    )
                    self.current_speed = random.uniform(8.0, 12.0)
                elif pattern == "chicane":
                    # Quick sharp zig-zag
                    self.target_x = self.x_pos + random.choice([-250, 250])
                    self.target_y = self.y_pos + random.choice([-150, 150])
                    self.current_speed = random.uniform(5.5, 7.5)
                else:
                    # Broad sweeping apex
                    self.target_x = random.uniform(margin, self.sw - margin)
                    self.target_y = random.uniform(margin, self.sh - margin)
                    self.current_speed = random.uniform(6.0, 9.0)

                # Clamp inside viewable display
                self.target_x = max(
                    margin, min(self.target_x, self.sw - margin)
                )
                self.target_y = max(
                    margin, min(self.target_y, self.sh - margin)
                )
            else:
                self.target_x = random.randint(50, self.sw - 150)
                self.target_y = random.randint(50, self.sh - 150)
                self.current_speed = 3.0

        next_interval = random.randint(2500, 5000)
        self.root.after(next_interval, self.pick_next_track_sector)

    def smooth_move_loop(self):
        """Runs at ~60 FPS so vehicle slides along track trajectories."""
        if not self.is_dragging:
            dx = self.target_x - self.x_pos
            dy = self.target_y - self.y_pos
            dist = math.hypot(dx, dy)

            if dist > self.current_speed:
                # Normalized directional movement
                self.x_pos += (dx / dist) * self.current_speed
                self.y_pos += (dy / dist) * self.current_speed
                self.root.geometry(f"+{int(self.x_pos)}+{int(self.y_pos)}")
                self.update_speech_position()

        self.root.after(16, self.smooth_move_loop)

    def try_to_speak(self):
        self.hide_speech()

        if self.pet_type == "lewis":
            phrases = [
                "Hammer time!",
                "Still we rise!",
                "Bono, my tyres are fine!",
                "For the Tifosi!",
                "Focus mode on.",
            ]
        elif self.pet_type == "f1":
            phrases = [
                "Simply lovely!",
                "Full throttle!",
                "Box, box, box!",
                "DRS enabled!",
            ]
        else:
            phrases = [
                "Hi Anika!",
                "Keep coding!",
                "Heads up Love",
                "Doing great!",
                "Focus up!",
                "Let's not forget why we're here!",
                "Guwnap",
            ]

        chosen = random.choice(phrases)

        self.speech_window = tk.Toplevel(self.root)
        self.speech_window.overrideredirect(True)
        self.speech_window.wm_attributes("-topmost", True)

        bubble_color = "#E10600" if self.pet_type == "lewis" else "#4E389E"
        txt_color = "white" if self.pet_type == "lewis" else "black"

        lbl = tk.Label(
            self.speech_window,
            text=chosen,
            bg=bubble_color,
            fg=txt_color,
            font=("Arial", 9, "bold"),
            bd=1,
            relief="solid",
            padx=8,
            pady=4,
        )
        lbl.pack()

        self.update_speech_position()

        # Auto dismiss after 4 seconds
        self.speech_timer = self.root.after(4000, self.hide_speech)

    def update_speech_position(self):
        """Anchors the active speech bubble above the pet at all times."""
        if self.speech_window and self.speech_window.winfo_exists():
            bubble_x = int(self.x_pos + 5)
            bubble_y = int(self.y_pos - 32)
            self.speech_window.geometry(f"+{bubble_x}+{bubble_y}")

    def hide_speech(self):
        if self.speech_timer:
            self.root.after_cancel(self.speech_timer)
            self.speech_timer = None
        if self.speech_window and self.speech_window.winfo_exists():
            self.speech_window.destroy()
        self.speech_window = None


if __name__ == "__main__":
    selected_pet = sys.argv[1] if len(sys.argv) > 1 else "default"
    root = tk.Tk()
    app = DesktopPet(root, pet_type=selected_pet)
    root.mainloop()