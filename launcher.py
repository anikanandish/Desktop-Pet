from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

SCRIPT_DIR = Path(__file__).resolve().parent
PET_SCRIPT = SCRIPT_DIR / "pet.py"

# Minimal single-accent theme
THEME = {
    "bg": "#0D0D11",
    "card": "#16161D",
    "hover": "#20202A",
    "border": "#262633",
    "accent": "#6366F1",       # Single cohesive accent (Electric Indigo)
    "fg_main": "#F8FAFC",
    "fg_sub": "#94A3B8",
}

PETS = [
    ("Max F1", "f1", "V10 Screamer - Built for speed"),
    ("Lewis LH44", "lewis", "#44 Hammer Time - Tifosi Edition"),
    ("Ayrton Senna", "senna", "King of Monaco - Gap seeker"),
    ("Purple Berry", "default", "Chill & bouncy companion"),
    ("Green Apple", "green_apple", "Crisp & energetic buddy"),
]


def launch_pet(pet_id: str):
    if not PET_SCRIPT.exists():
        messagebox.showerror("Error", f"Could not find '{PET_SCRIPT.name}' in:\n{SCRIPT_DIR}")
        return
    subprocess.Popen([sys.executable, str(PET_SCRIPT), pet_id], cwd=SCRIPT_DIR)
    root.destroy()


root = tk.Tk()
root.title("Desktop Pet Launcher")
root.geometry("380x560")
root.resizable(False, False)
root.configure(bg=THEME["bg"])
root.eval("tk::PlaceWindow . center")

# Header Section
header = tk.Frame(root, bg=THEME["bg"])
header.pack(fill="x", padx=24, pady=(24, 16))

tk.Label(
    header, text="Choose Companion", font=("Segoe UI", 16, "bold"),
    fg=THEME["fg_main"], bg=THEME["bg"]
).pack(anchor="w")

tk.Label(
    header, text="Select a pet to run on your desktop", font=("Segoe UI", 9),
    fg=THEME["fg_sub"], bg=THEME["bg"]
).pack(anchor="w", pady=(2, 0))

# Cards Container
container = tk.Frame(root, bg=THEME["bg"])
container.pack(fill="both", expand=True, padx=20, pady=(0, 20))


def create_card(parent, title, pet_id, subtitle):
    card = tk.Frame(
        parent, bg=THEME["card"],
        highlightbackground=THEME["border"], highlightthickness=1,
        cursor="hand2"
    )
    card.pack(fill="x", pady=6, ipady=3)

    accent_bar = tk.Frame(card, bg=THEME["accent"], width=3)
    accent_bar.pack(side="left", fill="y")

    info = tk.Frame(card, bg=THEME["card"])
    info.pack(side="left", fill="both", expand=True, padx=12, pady=8)

    lbl_title = tk.Label(
        info, text=title, font=("Segoe UI", 11, "bold"),
        fg=THEME["fg_main"], bg=THEME["card"]
    )
    lbl_title.pack(anchor="w")

    lbl_sub = tk.Label(
        info, text=subtitle, font=("Segoe UI", 8),
        fg=THEME["fg_sub"], bg=THEME["card"]
    )
    lbl_sub.pack(anchor="w", pady=(2, 0))

    # Unified hover state applied recursively to all child widgets
    interactive_widgets = [card, info, lbl_title, lbl_sub]

    def set_state(bg_color, border_color):
        card.config(bg=bg_color, highlightbackground=border_color)
        info.config(bg=bg_color)
        lbl_title.config(bg=bg_color)
        lbl_sub.config(bg=bg_color)

    for w in interactive_widgets:
        w.bind("<Enter>", lambda e: set_state(THEME["hover"], THEME["accent"]))
        w.bind("<Leave>", lambda e: set_state(THEME["card"], THEME["border"]))
        w.bind("<Button-1>", lambda e, pid=pet_id: launch_pet(pid))


for name, pet_id, subtitle in PETS:
    create_card(container, name, pet_id, subtitle)

root.mainloop()