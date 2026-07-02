import tkinter as tk
from PIL import Image, ImageTk
import os
import random

# Setup main window
root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "white")

# Load animation frames
frame_files = ["pet1.png", "pet2.png", "pet3.png"]
frames = []

for file in frame_files:
    if os.path.exists(file):
        img = Image.open(file).resize((100, 100))
        frames.append(ImageTk.PhotoImage(img))
    else:
        print(f"Missing image: {file}")
        root.destroy()
        exit()

# Display the first frame
label = tk.Label(root, image=frames[0], bg='white')
label.pack()

# Initial position
x_pos = 300
y_pos = 300
root.geometry(f"+{x_pos}+{y_pos}")

# Drag functionality
def start_drag(event):
    root.x = event.x
    root.y = event.y

def drag(event):
    global x_pos, y_pos
    x_pos = event.x_root - root.x
    y_pos = event.y_root - root.y
    root.geometry(f"+{x_pos}+{y_pos}")

label.bind("<Button-1>", start_drag)
label.bind("<B1-Motion>", drag)

# Right-click to close
label.bind("<Button-3>", lambda e: root.destroy())

#  Animate the pet
frame_index = 0
def animate():
    global frame_index
    frame_index = (frame_index + 1) % len(frames)
    label.config(image=frames[frame_index])
    root.after(300, animate)  # update frame every 300ms

#  Move pet randomly
def move_randomly():
    global x_pos, y_pos
    dx = random.choice([-20, -10, 0, 10, 20])
    dy = random.choice([-20, -10, 0, 10, 20])

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    x_pos = max(0, min(x_pos + dx, sw - 100))
    y_pos = max(0, min(y_pos + dy, sh - 100))

    root.geometry(f"+{x_pos}+{y_pos}")
    root.after(2000, move_randomly)

#  Start animation and movement
animate()
move_randomly()
root.mainloop()



