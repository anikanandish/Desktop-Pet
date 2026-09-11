import math
from pathlib import Path
import random
import sys
import tkinter as tk
from PIL import Image, ImageTk

SCRIPT_DIR = Path(__file__).resolve().parent

PET_CONFIG = {
    "senna": {
        "frames": ["senna1.png", "senna2.png", "senna3.png"],
        "is_car": True, "anim_delay": 140, "base_speed": 6.0,
        "bg": "#FEDB00", "fg": "#0B2B11",
        "phrases": [
            "If you no longer go for a gap...", "...you are no longer a racing driver.",
            "Pure commitment!", "Master of Monaco.", "Push to the limit!"
        ]
    },
    "lewis": {
        "frames": ["lh1.png", "lh2.png", "lh3.png"],
        "is_car": True, "anim_delay": 140, "base_speed": 6.0,
        "bg": "#E10600", "fg": "white",
        "phrases": ["Hammer time!", "Still we rise!", "For the Tifosi!", "Focus mode on."]
    },
    "f1": {
        "frames": ["f1_1.png", "f1_2.png", "f1_3.png"],
        "is_car": True, "anim_delay": 140, "base_speed": 6.0,
        "bg": "#4E389E", "fg": "white",
        "phrases": ["Simply lovely!", "Full throttle!", "Box, box, box!", "DRS enabled!"]
    },
    "green_apple": {
        "frames": ["green1.png", "green2.png", "green3.png"],
        "is_car": False, "anim_delay": 300, "base_speed": 3.0,
        "bg": "#2E7D32", "fg": "white",
        "phrases": ["Fresh and crisp!", "Crunch time!", "Stay healthy!"]
    },
    "default": {
        "frames": ["pet1.png", "pet2.png", "pet3.png"],
        "is_car": False, "anim_delay": 300, "base_speed": 3.0,
        "bg": "#4E389E", "fg": "white",
        "phrases": ["Keep coding!", "Doing great!", "Focus up!", "Let's build!"]
    }
}


class DesktopPet:
    def __init__(self, root: tk.Tk, pet_type: str = "default"):
        self.root = root
        self.cfg = PET_CONFIG.get(pet_type, PET_CONFIG["default"])
        
        # Transparent borderless canvas setup
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        try:
            self.root.wm_attributes("-transparentcolor", "white")
        except tk.TclError:
            pass  # Fallback gracefully for macOS/Linux

        self.sw, self.sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.x, self.y = 350.0, 350.0
        self.target_x, self.target_y = self.x, self.y
        self.speed = self.cfg["base_speed"]
        self.is_dragging = False
        self.current_heading = 0.0

        # Load raw images for rotation transformations
        self.raw_frames = self._load_raw_images()
        self.frame_idx = 0
        self.tk_image = ImageTk.PhotoImage(self.raw_frames[0])

        self.label = tk.Label(self.root, image=self.tk_image, bg="white", bd=0)
        self.label.pack()

        # Drag & exit controls
        self.label.bind("<Button-1>", self._start_drag)
        self.label.bind("<B1-Motion>", self._on_drag)
        self.label.bind("<ButtonRelease-1>", self._stop_drag)
        self.label.bind("<Button-3>", lambda e: self.root.destroy())

        self.speech_win, self.speech_timer = None, None

        # Main loops
        self._animate()
        self._pick_track_sector()
        self._physics_step()

    def _load_raw_images(self):
        images = []
        for file in self.cfg["frames"]:
            path = SCRIPT_DIR / file
            if not path.exists():
                print(f"Error: Asset '{path}' missing.")
                self.root.destroy()
                sys.exit(1)
            images.append(Image.open(path).convert("RGBA").resize((100, 100)))
        return images

    def _start_drag(self, event):
        self.is_dragging = True
        self.drag_offset_x = event.x
        self.drag_offset_y = event.y

    def _on_drag(self, event):
        self.x = float(event.x_root - self.drag_offset_x)
        self.y = float(event.y_root - self.drag_offset_y)
        self.target_x, self.target_y = self.x, self.y
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        self._sync_speech_pos()

    def _stop_drag(self, event):
        self.is_dragging = False
        self.say_something()

    def _animate(self):
        self.frame_idx = (self.frame_idx + 1) % len(self.raw_frames)
        frame = self.raw_frames[self.frame_idx]

        # Rotate cars in movement direction
        if self.cfg["is_car"] and self.current_heading:
            frame = frame.rotate(-self.current_heading, expand=False, resample=Image.BICUBIC)

        self.tk_image = ImageTk.PhotoImage(frame)
        self.label.config(image=self.tk_image)
        self.root.after(self.cfg["anim_delay"], self._animate)

    def _pick_track_sector(self):
        if not self.is_dragging:
            m = 120
            if self.cfg["is_car"]:
                mode = random.choice(["straight", "turn", "chicane"])
                if mode == "straight":
                    self.target_x = random.choice([m, self.sw - m])
                    self.speed = random.uniform(8.0, 12.0)
                else:
                    self.target_x = random.uniform(m, self.sw - m)
                    self.target_y = random.uniform(m, self.sh - m)
                    self.speed = random.uniform(5.5, 8.5)
            else:
                self.target_x = random.randint(50, self.sw - 150)
                self.target_y = random.randint(50, self.sh - 150)
                self.speed = self.cfg["base_speed"]

        self.root.after(random.randint(2500, 4500), self._pick_track_sector)

    def _physics_step(self):
        if not self.is_dragging:
            dx, dy = self.target_x - self.x, self.target_y - self.y
            dist = math.hypot(dx, dy)

            if dist > 1.0:
                step = min(self.speed, dist)
                self.x += (dx / dist) * step
                self.y += (dy / dist) * step
                self.current_heading = math.degrees(math.atan2(dy, dx))
                self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
                self._sync_speech_pos()

        self.root.after(16, self._physics_step)

    def say_something(self):
        self._dismiss_speech()
        phrase = random.choice(self.cfg["phrases"])

        self.speech_win = tk.Toplevel(self.root)
        self.speech_win.overrideredirect(True)
        self.speech_win.wm_attributes("-topmost", True)

        tk.Label(
            self.speech_win, text=phrase,
            bg=self.cfg["bg"], fg=self.cfg["fg"],
            font=("Arial", 9, "bold"), bd=1, relief="solid", padx=8, pady=4
        ).pack()

        self._sync_speech_pos()
        self.speech_timer = self.root.after(3500, self._dismiss_speech)

    def _sync_speech_pos(self):
        if self.speech_win and self.speech_win.winfo_exists():
            self.speech_win.geometry(f"+{int(self.x + 5)}+{int(self.y - 32)}")

    def _dismiss_speech(self):
        if self.speech_timer:
            self.root.after_cancel(self.speech_timer)
            self.speech_timer = None
        if self.speech_win and self.speech_win.winfo_exists():
            self.speech_win.destroy()
        self.speech_win = None


if __name__ == "__main__":
    pet_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    app = DesktopPet(tk.Tk(), pet_type=pet_name)
    app.root.mainloop()