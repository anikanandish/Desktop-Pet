import tkinter as tk
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PET_SCRIPT = SCRIPT_DIR / "pet.py"

def launch_pet(pet_name):
    print(f"Launching {pet_name}...")
    subprocess.Popen(
        [sys.executable, str(PET_SCRIPT), pet_name],
        cwd=SCRIPT_DIR
    )
    root.destroy()

root = tk.Tk()
root.title("Choose Your Desktop Pet")
root.geometry("300x230")
root.resizable(False, False)

tk.Label(root, text="Select a companion:", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="Purple Berry",
          command=lambda: launch_pet("default")).pack(pady=5)

tk.Button(root, text="Green Apple",
          command=lambda: launch_pet("green_apple")).pack(pady=5)

tk.Button(root, text="Max F1",
          command=lambda: launch_pet("f1")).pack(pady=5)

root.mainloop()

##### the racecar finally runssssssssssssssss
