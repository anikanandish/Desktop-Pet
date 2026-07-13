import tkinter as tk
import subprocess

def launch_pet(pet_name):
    print(f"Launching {pet_name}...")
    # This will eventually start your pet script and hand over the pet name!
    subprocess.Popen(["python", "pet.py"])
    root.destroy() # Closes the selection menu

# Create the selection window
root = tk.Tk()
root.title("Choose Your Desktop Pet")
root.geometry("300x200")

label = tk.Label(root, text="Select a companion:", font=("Arial", 12))
label.pack(pady=10)

# Buttons for your future pets!
btn1 = tk.Button(root, text="Purple Berry", command=lambda: launch_pet("purple_berry"))
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Green Apple", command=lambda: launch_pet("green_apple"))
btn2.pack(pady=5)

btn3 = tk.Button(root, text="Golden Mango", command=lambda: launch_pet("golden_mango"))
btn3.pack(pady=5)

btn4 = tk.Button(root, text="Blue Citrus", command=lambda: launch_pet("blue_citrus"))
btn4.pack(pady=5)

btn5 = tk.Button(root, text="Coming Soon...", state="disabled")
btn5.pack(pady=5)

root.mainloop()