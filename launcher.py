import subprocess
import sys
import tkinter as tk
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PET_SCRIPT = SCRIPT_DIR / "pet.py"

# Pet configurations: (Name, ID, Tagline/Emoji, Accent Color)
PETS = [
    ("Max F1", "f1", "  V10 Screamer - Built for speed", "#0A28A1"),
    ("Purple Berry", "default", "  Chill & bouncy companion", "#8A2BE2"),
    ("Green Apple", "green_apple", " Crisp & energetic buddy", "#2ECC71"),
    ########hyy
]


def launch_pet(pet_id):
    print(f"Launching {pet_id}...")
    subprocess.Popen([sys.executable, str(PET_SCRIPT), pet_id], cwd=SCRIPT_DIR)
    root.destroy()


# --- Main Window Setup ---
root = tk.Tk()
root.title("Desktop Pet Launcher")
root.geometry("380x420")
root.resizable(False, False)
root.configure(bg="#121214")

# Center window on screen
root.eval("tk::PlaceWindow . center")

# Header Section
header_frame = tk.Frame(root, bg="#121214")
header_frame.pack(fill="x", padx=24, pady=(24, 16))

tk.Label(
    header_frame,
    text="Choose Companion",
    font=("Segoe UI", 16, "bold"),
    fg="#FFFFFF",
    bg="#121214",
).pack(anchor="w")

tk.Label(
    header_frame,
    text="Select a pet to run on your desktop",
    font=("Segoe UI", 9),
    fg="#8E8E93",
    bg="#121214",
).pack(anchor="w", pady=(2, 0))

# --- Interactive Pet Cards ---
cards_frame = tk.Frame(root, bg="#121214")
cards_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))


def create_card(parent, title, pet_id, subtitle, accent):
    card = tk.Frame(
        parent,
        bg="#1E1E24",
        highlightbackground="#2A2A32",
        highlightthickness=1,
        cursor="hand2",
    )
    card.pack(fill="x", pady=6, ipady=4)

    # Left color strip
    accent_bar = tk.Frame(card, bg=accent, width=4)
    accent_bar.pack(side="left", fill="y")

    # Content container
    info_frame = tk.Frame(card, bg="#1E1E24")
    info_frame.pack(side="left", fill="both", expand=True, padx=12, pady=8)

    title_lbl = tk.Label(
        info_frame,
        text=title,
        font=("Segoe UI", 11, "bold"),
        fg="#F5F5F7",
        bg="#1E1E24",
    )
    title_lbl.pack(anchor="w")

    sub_lbl = tk.Label(
        info_frame,
        text=subtitle,
        font=("Segoe UI", 8),
        fg="#9A9AA2",
        bg="#1E1E24",
    )
    sub_lbl.pack(anchor="w", pady=(2, 0))

    # Hover animations
    def on_enter(e):
        card.config(bg="#282830", highlightbackground=accent)
        info_frame.config(bg="#282830")
        title_lbl.config(bg="#282830")
        sub_lbl.config(bg="#282830")

    def on_leave(e):
        card.config(bg="#1E1E24", highlightbackground="#2A2A32")
        info_frame.config(bg="#1E1E24")
        title_lbl.config(bg="#1E1E24")
        sub_lbl.config(bg="#1E1E24")

    def on_click(e):
        launch_pet(pet_id)

    # Bind events across all child widgets in the card
    for w in (card, info_frame, title_lbl, sub_lbl):
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
        w.bind("<Button-1>", on_click)


for name, pet_id, subtitle, accent_color in PETS:
    create_card(cards_frame, name, pet_id, subtitle, accent_color)

root.mainloop()
